import json
from langchain_community.llms import HuggingFaceHub
from langchain.chains import LLMChain, ConversationChain
from langchain.prompts import PromptTemplate
from langchain.memory import ChatMessageHistory, ConversationBufferMemory,ConversationSummaryMemory
from langchain_community.chat_models import ChatOpenAI
from langchain_openai import OpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings

# Öffne die JSON-Datei und lade den Inhalt
with open('/Users/riccardo/Desktop/Repositorys_Github/LLM/Docs/api_token.json', 'r') as api_file:
    api_token_file = json.load(api_file)

# Extrahiere die Variable aus den Daten
api_token = api_token_file['Hugging_face_token']






class LLM_Mistral:


    """
    Eine Klasse, um mit einem Sprachmodell zu interagieren.
    """
    def __init__(self, api_token:str, question:str):
        self.api_token = api_token
        self.llm = self._set_llm_model()
        self.question = question

        


    def _set_llm_model(self):
        """
        Diese Funktion erlaubt es den nutzer sein API Token zu setzen und das Sprachmodell zu initialisieren.
        Das Modell ist das von Mistral-7B-Instruct-v0.2

        - Input: 
            api_token = ist das API Token als String

        - Output: 
            Das Sprachmodell
        """

        llm = HuggingFaceHub(repo_id='mistralai/Mistral-7B-Instruct-v0.2', 
                              huggingfacehub_api_token=self.api_token)
        
        return llm
    

    def _template(self,question):
        """
        Create a Templeate how the LLM should behave as a agent.

        Input:
            - question = The question that the LLM should answer
        Output:
            - llm_chain = The LLM Chain with the template
        """
        if self._set_llm_model():
            template = "You are an artificial intelligence assistant, answer the question. {question}"
            prompt = PromptTemplate(template=template, input_variables=["question"])
            llm_chain = LLMChain(prompt=prompt, llm=self.llm)
            return llm_chain
    

    def _ask_a_question(self, question:str):
        """
        Ask a question to the LLM model.
        """
        if self._template(self.question):
            llm_chain = self._template(question)
            output = llm_chain.invoke(question)
            return output
        if self._template(question) == False:
            return "Error: Language model not initialized."


# Example usage:




response = {
    'question': 'What makes Osnabrück in germany so great?', 
    'text': 'Osnabrück, a city located in northwest Germany, is known for several unique features that make it a great place to live, work, and visit. Here are some reasons why Osnabrück is considered special:\n\n1. Rich History: Osnabrück has a rich and diverse history. The city was founded in 1224 and has been an important trading center and cultural hub for centuries. It was also the site of the Peace'
}

question = response['question']
mistral = LLM_Mistral(api_token, question)

response = mistral._ask_a_question(question)





print(response['text'])
