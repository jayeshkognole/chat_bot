from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
import google.generativeai as genai
import configparser
from utils.prompt import CHAT_PROMPT,NORMAL_CHAT_PROMPT
from utils.gemini import Gemini
from utils.rag import rag_pipeline
from services.database_service import get_conversational_history
config = configparser.ConfigParser()
config.read('config.ini')



gemini = Gemini()
    
def get_gemini_response(prompt, language='en', context_length='medium', include_history=True,chat_tab_id=""):
    conversation_history=[]
    if include_history:
        conversations=get_conversational_history(chat_tab_id)
        latest_conversations = conversations[-4:]
        for conversation in reversed(latest_conversations):
            message=dict()
            message['question']=conversation['user_message']
            message['answer']=conversation['ai_response']
            conversation_history.append(message)
        conversation_history.reverse()

    print(f"{conversation_history}\n\n\n")
    final_prompt=NORMAL_CHAT_PROMPT.replace("{question}",prompt).replace("{history}",str(conversation_history if len(conversation_history)>0 else ""))
    return gemini.get_text_response(str(final_prompt))

def get_rag_response(prompt, pdf_paths, language='en', context_length='medium', include_history=True,chat_tab_id=""):
    conversation_history=[]
    if include_history:
        conversations=get_conversational_history(chat_tab_id)
        for conversation in conversations:
            message=dict()
            message['question']=conversation['user_message']
            message['answer']=conversation['ai_response']
            conversation_history.append(message)
    documents,metadata=rag_pipeline(prompt,pdf_paths)
    final_prompt=CHAT_PROMPT.replace("{question}",prompt).replace("{language}",language).replace("{context}",str(documents)).replace("{history}",str(conversation_history if len(conversation_history)>0 else ""))
    response=gemini.get_text_response(final_prompt)
    return response,metadata
