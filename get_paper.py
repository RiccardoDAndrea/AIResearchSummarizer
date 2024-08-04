import requests
from bs4 import BeautifulSoup
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import PyPDFLoader
import requests
import fitz # PyMuPDF
import os


def check_and_create_folder():
    """
    Check if the folder exists and if not create it
    """
    if os.path.exists('PDF_docs'):
        pass
    else:
        os.mkdir('PDF_docs')



def getPaper(url: str):  
    """
    Eine Funktion, die das ganze Paper der Webseite https://www.jmlr.org/ abruft von der aktuellsten Veröffentlichung Paper
    Input:
        - url: string
    Output:
        - latest_paper_link: string
    """
    response = requests.get(url)  # Abrufen der Webseite
    
    if response.status_code == 200:  # Statuscode 200 bedeutet, dass die Anfrage erfolgreich war
        text = response.text
        soup = BeautifulSoup(text, 'html.parser')  # Erstelle ein BeautifulSoup-Objekt form html code
        paper_links = soup.find_all('a', href=True)  # Finde alle Links auf der Webseite
        meta_data_ = [paper_link['href'] for paper_link in paper_links if paper_link['href'].endswith('.pdf')]  # Finde alle Links die auf .pdf enden
        
        if meta_data_:
            latest_paper = meta_data_[0]
            latest_paper_link = 'https://www.jmlr.org' + latest_paper
            str_latest_paper_link = ''.join(latest_paper_link)
            return str_latest_paper_link, latest_paper
        
    else: 
        print("Error: ", response.status_code)
    return None


def save_paper(url:str):
    link_to_paper, file_name = getPaper('https://www.jmlr.org')
    # Download the PDF
    splitByComma=file_name.split('/')
    name_of_file = splitByComma.pop()

    download_pdf(link_to_paper, name_of_file)
    return name_of_file


def get_Abstract(url: str):
    """
    Eine Funktion, die das Abstract der Webseite https://www.jmlr.org/ abruft von der aktuellsten Veröffentlichung Paper
    Input:
        - url: string
    Output:
        - latest_paper_link: string
    """
    response = requests.get(url)                                    # Abrufen der Webseite
    if response.status_code == 200:                                 # status code 200 bedeutet, dass die Anfrage erfolgreich war
        text = response.text                                        # Inhalt der Webseite html code
        soup = BeautifulSoup(text, 'html.parser')                   # Erstelle ein BeautifulSoup-Objekt form html code
        paper_links = soup.find_all('a', href=True)                 # Finde alle Links auf der Webseite 
        meta_data_ = [paper_link['href'] for paper_link in paper_links if paper_link['href'].endswith('.html')] # Finde alle Links die auf .html enden für die Abstract-Seite
        
        ergebnis = [paper_link for paper_link in meta_data_ if '/papers/' in paper_link][0] # Wähle den Link der auf /papers/ endet
        webpage_abs = url + ergebnis
        return webpage_abs


def get_Meta_Info(url: str):
    """
    Input
    - url: URL of the JMLR website
    Output
    - meta_data: string with the Author, Title and Abstract and so on
    """
    response = requests.get(url)  # Abrufen der Webseite
    
    if response.status_code == 200:  # Bei erfolgreichem Abrufen der Webseite
        text = response.text  # Inhalt der Webseite HTML-Code
        soup = BeautifulSoup(text, 'html.parser')  # Erstelle ein BeautifulSoup-Objekt vom HTML-Code
        paper_links = soup.find_all('a', href=True)  # Finde alle Links auf der Webseite
        meta_data_ = [link['href'] for link in paper_links if link['href'].endswith('.bib')]  # Finde alle Links, die auf .bib enden für die Metadaten
        
        if not meta_data_:
            return "No metadata link found."
        
        meta_data = meta_data_[0]  # Wähle den aktuellsten Link
        ergebnis_meta_info = url + meta_data
        meta_information = requests.get(ergebnis_meta_info).text
        
        title_match = re.search(r'title\s*=\s*\{(.+?)\}', meta_information, re.IGNORECASE)
        author_match = re.search(r'author\s*=\s*\{(.+?)\}', meta_information, re.IGNORECASE)
        
        title = title_match.group(1) if title_match else "Title not found"
        author = author_match.group(1) if author_match else "Author not found"

        result = "Title: '" + str(title) + "'" + " " + ", Author : " + "'" + str(author) + "'"

        return result
    else:
        return f"Error: {response.status_code}"
   

def text_splitter():
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

def PyPDFLoader_papers(pdf = str):
    """
    Initialisiert den WebBaseLoader

    Input:
        - None

    Output:
        - loader: Ein Objekt des WebBaseLoader
    """
    
    loader = PyPDFLoader(pdf)
    pages = loader.load_and_split()
    return pages


 

def get_all_information(url:str):
    """
    Get all information from the website
    """
    
    paper_link = getPaper(url)
    abstract_link = get_Abstract(url)
    title, author = get_Meta_Info(url)
    return paper_link, abstract_link, title, author


def download_pdf(url: str, filename: str):
    """
    Downloads a PDF file from a URL and saves it locally.
    
    Input:
    - url: The URL of the PDF file
    - filename: The local filename to save the PDF as
    """
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded PDF and saved as {filename}")
    else:
        print(f"Failed to download PDF. Status code: {response.status_code}")


def extract_text_from_pdf(filename: str):
    """
    Extracts text from a PDF file using PyMuPDF.
    
    Input:
    - filename: The local filename of the PDF
    
    Output:
    - text: Extracted text from the PDF
    """
    try:
        document = fitz.open(filename)
        text = ""
        for page_num in range(document.page_count):
            page = document.load_page(page_num)
            text += page.get_text()
        return text
    except Exception as e:
        return f"An error occurred: {e}"

# URL of the PDF and the local filename to save it as
#pdf_url = getPaper('https://www.jmlr.org')

#extracted_text = extract_text_from_pdf(file_name)


    # Extract text from the downloaded PDF




check_and_create_folder()


        
# Test the functions
#print(getPaper('https://www.jmlr.org'))
#print(get_Meta_Info('https://www.jmlr.org'))
#print(get_Abstract('https://www.jmlr.org'))
#print(extract_title_and_author(get_Meta_Info('https://www.jmlr.org')))

#print(get_all_information('https://www.jmlr.org'))