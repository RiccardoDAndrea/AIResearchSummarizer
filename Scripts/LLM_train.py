import json
from langchain_community.llms import HuggingFaceHub
from langchain.chains import LLMChain, ConversationChain
from langchain.prompts import PromptTemplate
from langchain.memory import ChatMessageHistory, ConversationBufferMemory,ConversationSummaryMemory
from langchain_community.chat_models import ChatOpenAI
from langchain_openai import OpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings

with open('/Users/riccardo/Desktop/Repositorys_Github/LLM/Docs/api_token.json', 'r') as api_file:
    api_token_file = json.load(api_file)

# Extrahiere die Variable aus den Daten
api_token = api_token_file['Hugging_face_token']
open_ai_token = api_token_file['Open_api_token']


llm = HuggingFaceHub(repo_id='mistralai/Mistral-7B-Instruct-v0.2', huggingfacehub_api_token=api_token)

question = 'Where is Langchain?'
output = llm.invoke(question)
print(output)

class LLM:
    """
    
    
    """
    def __init__(self, api_token, llm):
        self.llm = llm
        self.api_token = api_token

    def set_llm_model(self, api_token):
        """
        
        """
        llm = HuggingFaceHub(repo_id='mistralai/Mistral-7B-Instruct-v0.2', 
                             huggingfacehub_api_token=api_token)
        
        return llm