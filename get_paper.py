import requests
from bs4 import BeautifulSoup
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import PyPDFLoader
import requests
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
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
            separators="\n",
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
        chunks = []
            # Check if the "PDF_docs" directory exists and has files
        if os.path.exists("PDF_docs") and os.listdir("PDF_docs"):
            directory_path = os.path.join("PDF_docs", os.listdir("PDF_docs")[0])
            if directory_path.endswith('.pdf'):
                loader = PyPDFLoader(directory_path)
        chunks += loader.load_and_split()
        print(chunks)
        
                
        return chunks

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
            db = Chroma.from_documents(chunks, embedding_function)
            

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
                              huggingfacehub_api_token = API_Key)
        return llm


        


import json

def get_keys(path):
    with open(path) as f:
        return json.load(f)
keys = get_keys("secret_File.json")
API_Key = keys['API_Key']

print(API_Key)



chatbot = Paper_to_Chatbot(url="https://www.jmlr.org/")

# Schritt 1: Papier abrufen und herunterladen
pdf_url, filename = chatbot.getPaper()
if pdf_url and filename:
    chatbot.download_pdf(pdf_url, filename)

# Schritt 2: Text in Chunks aufteilen
chunks = chatbot.chunks()

# Schritt 3: Chroma-Datenbank initialisieren
db = chatbot.initialise_chroma()

# Schritt 4: Abfrage stellen
#query = "What is the main contribution of the paper?"
query = "What does the paper 'BenchMARL: Benchmarking Multi-Agent Reinforcement?' talk about?"
documents = chatbot.retriever(query)

# Schritt 5: Antwort generieren
answer = chatbot.llm_model().invoke(query)
print(answer)


