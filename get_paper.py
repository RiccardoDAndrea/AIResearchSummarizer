import requests
from bs4 import BeautifulSoup
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import PyPDFLoader
import requests
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
import fitz # PyMuPDF
import os
from langchain_community.llms import HuggingFaceEndpoint
from langchain.chains import RetrievalQAWithSourcesChain



class Paper_to_Chatbot:
    def __init__(self, url: str):
        self.url = url

    def check_and_create_folder(self):
        """
        Check if the folder exists and if not create it.
        """
        folder = 'PDF_docs'
        if os.path.exists(folder):
            print("Folder exists")
            return True
        else:
            os.mkdir(folder)
            print("Folder created")
            return False

    def getPaper(self):
        """
        A function that retrieves the latest paper from the website https://www.jmlr.org/ of the most recent publication.
        Input:
            - url: str (example https://www.jmlr.org/)
        Output:
            - latest_paper_link: string (example https://www.jmlr.org/papers/volume25/23-1612/23-1612.pdf)
            - name_of_file: string (example 23-1612.pdf)
        """
        if self.check_and_create_folder():
            response = requests.get(self.url)  # Fetch the webpage

            if response.status_code == 200:  # Status code 200 means the request was successful
                soup = BeautifulSoup(response.text, 'html.parser')  # Create a BeautifulSoup object from the HTML code
                paper_links = soup.find_all('a', href=True)  # Find all links on the webpage

                pdf_links = [link['href'] for link in paper_links if link['href'].endswith('.pdf')]  # Find all links ending with .pdf

                if pdf_links:
                    latest_paper_link = pdf_links[0]  # get the first item of the list
                    latest_paper_url = self.url + latest_paper_link  # create the full URL
                    name_of_file = latest_paper_link.split('/')[-1]  # return 23-1612.pdf as example
                    return latest_paper_url, name_of_file

                else:
                    print("No PDF links found.")
                    return None, None

            else:
                print(f"Error: {response.status_code}")
                return None, None

    def getAbstract(self):
        """
        A function that retrieves the abstract from the website https://www.jmlr.org/ of the most recent publication.
        Input:
            - url: string
        Output:
            - abstract_text: string
        """
        response = requests.get(self.url)  # Fetch the webpage
        if response.status_code == 200:  # status code 200 means the request was successful
            text = response.text  # Content of the webpage html code
            soup = BeautifulSoup(text, 'html.parser')  # Create a BeautifulSoup object from the HTML code
            paper_links = soup.find_all('a', href=True)  # Find all links on the webpage

            # Find all links ending with .html for the abstract page
            meta_data_ = [paper_link['href'] for paper_link in paper_links if paper_link['href'].endswith('.html')]

            ergebnis = [paper_link for paper_link in meta_data_ if '/papers/' in paper_link][0]  # Select the link ending with /papers/
            _text = WebBaseLoader(self.url + ergebnis)
            data = _text.load()
            abstract_text = data[0].page_content.split('Abstract\n\n\n')[1].split('\n\n\n')[0]

            return abstract_text

    def download_pdf(self, pdf_url: str, filename: str):
        """
        Downloads a PDF file from a URL and saves it locally.
        
        Input:
        - pdf_url: The URL of the PDF file
        - filename: The local filename to save the PDF as
        """
        try:
            full_path = os.path.join('PDF_docs', filename)
            response = requests.get(pdf_url)
            if response.status_code == 200:
                with open(full_path, 'wb') as file:
                    file.write(response.content)
                print(f"Downloaded PDF and saved as {full_path}")

            else:
                print(f"Failed to download PDF. Status code: {response.status_code}")

        except Exception as e:
            print(f"An error occurred: {e}")

    def text_splitter(self):
        """
        Initializes the text splitter.

        Input:
            - None

        Output:
            - text_splitter: An object of the text splitter
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=200,
            chunk_overlap=50,
            length_function=len)
        return text_splitter

    def chunks(self):
        """
        Splits the abstract text into chunks.

        Input:
            - None

        Output:
            - chunks: List of text chunks or None if no abstract text is found
        """
        abstract_text = self.getAbstract()
        if abstract_text:
            text_splitter = self.text_splitter()
            chunks = text_splitter.split_text(abstract_text)
            print(chunks)
            # # Check if the "PDF_docs" directory exists and has files
            # if os.path.exists("PDF_docs") and os.listdir("PDF_docs"):
            #     directory_path = os.path.join("PDF_docs", os.listdir("PDF_docs")[0])
                
            #     if directory_path.endswith('.pdf'):
            #         loader = PyPDFLoader(directory_path)
            #         chunks += loader.load_and_split()
            #         print(chunks)
                
            #     else:
            #         print("No PDF files found in the directory.")
            # else:
            #     print("PDF_docs directory is empty or does not exist.")
                
            return chunks
            
        else:
            print("No abstract text found.")
            return None

    def embedding(self):
        """
        Returns a model with sentence embeddings.
        Input: 
            - None

        Output: 
            - embedding_function
        """
        embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        return embedding_function

    def initialise_chroma(self):
        """
        Initializes the Chroma database.
        Input:
            - None

        Output:
            - db: The Chroma database
        """
        chunks = self.chunks()
        if chunks:
            
            embedding_function = self.embedding()
        
            #db = Chroma.from_documents(chunks, embedding_function)
            db = Chroma.from_texts(chunks, embedding_function)

            return db
        else:
            print("No chunks found to initialize the database.")
            return None

    def retriever(self, query: str):
        """
        Initializes the retriever for the external data sources and returns the relevant documents.
        
        Input:
            - query: The query string
        
        Output:
            - retriever: The relevant documents
        """
        db = self.initialise_chroma()
        if db:
            retriever = db.as_retriever(search_kwargs={"k": 2})
            documents = retriever.get_relevant_documents(query)
            return documents
        else:
            print("No database initialized.")
            return None
        
    def llm_model(self):
        """
        Initialisiert das OpenAI-Modell. Hier wird das OpenAI modell genutzt für das RAG Modell
        
        Input:
            - None
        
        Output:
            - das LLM Modell von OpenAI
        """
        
        llm = HuggingFaceEndpoint(repo_id='mistralai/Mistral-7B-Instruct-v0.2', 
                              huggingfacehub_api_token = API_Key,
                              )
        return llm
    
    def qa_with_sources(self, query):
        """
        Die Funktion die die Frage beantwortet und die Quellen zurückgibt
        Input:
            - query: Die die Frage beinhalet
        Output:
            - qa_with_sources: Die Antwort auf die Frage und die Quellen
        
        """

        llm = self.llm_model()
        text_splitter_instance = self.text_splitter()
        chunks = self.loader_for_chunks(text_splitter_instance)
        embedding_instance = self.embedding()
        retriever_instance = self.retriever(Chroma.from_documents(chunks, embedding_instance), query)
        qa_with_sources = RetrievalQAWithSourcesChain.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever_instance)
        
        return qa_with_sources.invoke(query)



import json

def get_keys(path):
    with open(path) as f:
        return json.load(f)
keys = get_keys("secret_File.json")
API_Key = keys['API_Key']

print(API_Key)


# Beispielverzeichnis


# Die letzte Datei finden








# Example usage
if __name__ == "__main__":
    url = "https://www.jmlr.org/"
    query = "What is the latest paper about?"
    paper_to_chatbot = Paper_to_Chatbot(url)
    latest_paper_url, filename = paper_to_chatbot.getPaper()
    if latest_paper_url and filename:
        paper_to_chatbot.download_pdf(latest_paper_url, filename)
    documents = paper_to_chatbot.retriever(query)
    if documents:
        for doc in documents:
            print(doc)

