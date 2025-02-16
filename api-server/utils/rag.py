import os
import fitz 
import faiss
import numpy as np
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import configparser
config = configparser.ConfigParser()
config.read('config.ini')

gemini_api_key = config['GEMINI']['api_key']

EMBEDDING_MODEL = config['RAG']['embedding_model']
FAISS_INDEX_PATH = config['RAG']['faiss_index_path']
CHUNK_SIZE = int(config['RAG']['chunk_size'])
CHUNK_OVERLAP = int(config['RAG']['chunk_overlap'])
os.environ["GOOGLE_API_KEY"] = gemini_api_key


def format_response(data):
    result = {}
    for entry in data:
        filename = entry['filename']
        page = entry['page']
        if filename not in result:
            result[filename] = {page}
        else:
            result[filename].add(page)
    for filename in result:
        result[filename] = sorted(list(result[filename]))

    return result

def rag_pipeline(query: str, files):
    # 1. Load and Chunk PDFs using PyMuPDF
    documents = []
    metadata = []  # Store metadata (filename, page number)
    for filename in files:
        if filename.endswith(".pdf"):
            filepath = filename
            try:
                with fitz.open(filepath) as doc:  # Open PDF with PyMuPDF
                    page_num = 0
                    for page in doc:
                        page_num += 1
                        text = page.get_text()  # Extract text from each page
                        text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
                        chunks = text_splitter.split_text(text)
                        documents.extend(chunks)
                        metadata.extend([{"filename": filename, "page": page_num}] * len(chunks)) # Associate metadata with each chunk
            except Exception as e:
                print(f"Error processing {filename}: {e}")

    # 2. Create/Load FAISS Index
    if not os.path.exists(FAISS_INDEX_PATH):
        embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL).embed_documents(documents)
        dimension = len(embeddings[0])
        index = faiss.IndexFlatL2(dimension)
        index.add(np.array(embeddings).astype('float32'))
        faiss.write_index(index, FAISS_INDEX_PATH)
    else:
        index = faiss.read_index(FAISS_INDEX_PATH)

    # 3. Retrieve Relevant Documents
    query_embedding = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL).embed_query(query)
    D, I = index.search(np.array([query_embedding]).astype('float32'), 100) 

    # Deduplicate results based on filename and page number
    seen_metadata = set()
    unique_documents = []
    unique_metadata = []

    for i in I[0].tolist():
        metadata_tuple = (metadata[i]['filename'], metadata[i]['page'])
        if metadata_tuple not in seen_metadata:
            unique_documents.append(documents[i])
            unique_metadata.append(metadata[i])
            seen_metadata.add(metadata_tuple)
    os.remove(FAISS_INDEX_PATH)
    return str(unique_documents), format_response(unique_metadata)
