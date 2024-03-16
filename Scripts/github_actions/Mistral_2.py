from langchain_community.llms import HuggingFaceEndpoint
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.chains import RetrievalQAWithSourcesChain
import requests
from bs4 import BeautifulSoup
from langchain_community.document_loaders import WebBaseLoader
import os
from datetime import datetime

os.environ["TOKENIZERS_PARALLELISM"] = "false"
HUGGINGFACEAPI_TOKEN = os.environ.get('HUGGINGFACE_API_TOKEN')

# Strategie:
# Entwicklung eines OpenAI LLM RAG Modell:

# Erstellen einer Klasse (class) für ein OpenAI Language Model (LLM), das in der Lage ist, Fragen zu beantworten aus exterenen Datenquellen.
# Automatisierte Datenextraktion und -verarbeitung:

# Implementierung eines automatisierten Systems zur Extraktion und Verarbeitung von Daten aus PDF-Dokumenten.
# Die Daten werden im Verzeichnis /Users/riccardo/Desktop/Repositorys_Github/LLM/Docs/docs_for_llm_pipline gesammelt.
# Die extrahierten Daten werden zu einem großen PDF-Dokument zusammengeführt.
# Ausführung eines GitHub-Action-Skripts:

# Einrichten eines GitHub-Action-Skripts, das die PDFs automatisch zusammenführt und verarbeitet.
# Diese Strategie ermöglicht die nahtlose Integration von automatisierter Datenerfassung und -verarbeitung mit einem leistungsstarken OpenAI Language Model, um präzise Antworten auf Fragen bereitzustellen.


# Öffne die JSON-Datei und lade den Inhalt

# Extrahiere die Variable aus den Daten


class Mistral7B_RAG:
    """
    Eine Klasse die ein OpenAI-Modell initialisiert und eine Frage beantwortet.
    Input: 
        - Ist die Frage als Varaible query

    Output:
        - Die Antwort auf die Frage
    
    """

    def __init__(self, HUGGINGFACEAPI_TOKEN: str):
        self.HUGGINGFACEAPI_TOKEN = HUGGINGFACEAPI_TOKEN

    def text_splitter(self):
        """
        Initialisiert den Text-Splitter

        Input:
            - None

        Output:
            - text_splitter: Ein Objekt des Text-Splitters
        """
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=200,
            chunk_overlap=50, 
            length_function=len,
            
        )

        return text_splitter

    def loader_for_chunks(self, text_splitter):
        """
        Initialisiert den Loader für die Chunks mit der externen Datenquelle

        Input:
            - text_splitter: Ein Objekt des Text-Splitters aus der function text_splitter()
            - filepath: Der Pfad zur externen Datenquelle (z.B. eine PDF-Datei)

        Output:
            - chunks: Die Chunks der externen Datenquelle
        """
        # Annahme: Die Methode initialize() gibt Autor, Titel und Abstract zurück
        response = requests.get("https://www.jmlr.org")                                    # Abrufen der Webseite
        if response.status_code == 200:                                 # status code 200 bedeutet, dass die Anfrage erfolgreich war
            text = response.text                                        # Inhalt der Webseite html code
            soup = BeautifulSoup(text, 'html.parser')                   # Erstelle ein BeautifulSoup-Objekt form html code
            paper_links = soup.find_all('a', href=True)                 # Finde alle Links auf der Webseite 
            meta_data_ = [paper_link['href'] for paper_link in paper_links if paper_link['href'].endswith('.html')] # Finde alle Links die auf .html enden für die Abstract-Seite
            
            ergebnis = [paper_link for paper_link in meta_data_ if '/papers/' in paper_link][0] # Wähle den Link der auf /papers/ endet
            webpage_abs = "https://www.jmlr.org"+ ergebnis

        if response.status_code == 200:                                     # bei erfolgreich abrufen der Webseite
            text = response.text                                            # Inhalt der Webseite html code
            soup = BeautifulSoup(text, 'html.parser')                       # Erstelle ein BeautifulSoup-Objekt form html code
            paper_links = soup.find_all('a', href=True)                     # Finde alle Links auf der Webseite
            meta_data_ = [link['href'] for link in paper_links if link['href'].endswith('.bib')] # Finde alle Links die auf .bib enden für die Metadaten
            meta_data = meta_data_[0]                                       # Wähle den akutellsten Link
            ergebnis_meta_info = "https://www.jmlr.org" + meta_data   



        loader = WebBaseLoader([webpage_abs , ergebnis_meta_info]) # Erstelle ein WebBaseLoader-Objekt
        chunks = loader.load_and_split()

        return chunks

    def embedding(self):
        """
        Gibt ein Model mit Sentence-Embeddings zurück
        Input: 
            - None

        Output: 
            - embedding_function
        """

        embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

        return embedding_function

    def initialise_chroma(self, chunks, embedding_function):
        """
        
        Initialisiert die Chroma Datenbank
        Input:
            - chunks: Die Chunks der Exteren Datenquelle
            - embedding_function: Ein Objekt des Sentence-Embeddings

        Output:
            - db: Die Chroma Datenbank
        """

        db = Chroma.from_documents(chunks, embedding_function)

        return db
    
    def retriever(self, db, query):
        """
        Initialisiert den Retriever für die externe Datenquellen und gibt die relevanten Dokumente zurück aus der Quelle
        filepath = '/Users/riccardo/Desktop/Repositorys_Github/LLM/Docs/merged.pdf'

        Input:
            - db: Die Chroma Datenbank
            - query: Die Frage
        
        Output:
            - retriever: Die relevanten Dokumente
        
        """

        retriever = db.as_retriever(search_kwargs={"k": 2})
        retriever.get_relevant_documents(query)
        
        return retriever

    def llm_model(self):
        """
        Initialisiert das OpenAI-Modell. Hier wird das OpenAI modell genutzt für das RAG Modell
        
        Input:
            - None
        
        Output:
            - das LLM Modell von OpenAI
        """
        
        llm = HuggingFaceEndpoint(repo_id='mistralai/Mistral-7B-Instruct-v0.2', 
                              huggingfacehub_api_token= self.HUGGINGFACEAPI_TOKEN,
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

# Erstelle eine Instanz der Klasse OpenAI_RAG
openai_rag = Mistral7B_RAG(HUGGINGFACEAPI_TOKEN)


# datetime object containing current date and time

# Formatieren des Datums und der Uhrzeit
# Ändere das Format entsprechend deinen Anforderungen
# Stelle eine Frage und erhalte die Antwort
query = "Can you give me the authors, title and summaries the abstract?"

antwort = openai_rag.qa_with_sources(query)

# Gib die Antwort aus
print("Antwort:", antwort)



### sending message
body = f"""
Good day Herr DAndrea,
here you have your newest updated in the AI World
{antwort}


"""

# C R E A T E _ M A I L 
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl

# Define email parameters
port = 465
smtp_server = "smtp.gmail.com"
USER_EMAIL = os.environ.get('USER_EMAIL')
USER_PASSWORD = os.environ.get('USER_PASSWORD')

subject = "GitHub Email Report"

# Create email message
message = MIMEMultipart()
message['From'] = USER_EMAIL
message['To'] = USER_EMAIL
message['Subject'] = subject

# Attach the body to the email
message.attach(MIMEText(body, "plain"))

# Establish a secure connection with the SMTP server
context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    # Log in to the email server
    server.login(USER_EMAIL, USER_PASSWORD)
    # Send email
    server.sendmail(USER_EMAIL, USER_EMAIL, message.as_string())

print("E-Mail wurde erfolgreich gesendet.")