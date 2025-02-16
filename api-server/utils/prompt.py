CHAT_PROMPT="""

DOCUMENT:
{context}

CONVERSATION_HISTORY - {history}

QUESTION:
{question}

INSTRUCTIONS:
Answer the provided users QUESTION using the DOCUMENT text above.
Keep your answer ground in the facts of the DOCUMENT.
If the DOCUMENT doesn’t contain the facts to answer the QUESTION return Not found
provide response in this language : {language}"""


NORMAL_CHAT_PROMPT="""You are a helpful assistant 
refer the conversation history : {history} 
and answer this question : {question}
Provide the answer 
"""