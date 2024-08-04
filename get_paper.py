import requests
from bs4 import BeautifulSoup
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import PyPDFLoader
import requests
import fitz # PyMuPDF
import os

class Paper_to_Chatbot:
    
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

    def getPaper(self, url: str):
        """
        A function that retrieves the latest paper from the website https://www.jmlr.org/ of the most recent publication.
        Input:
            - url: str (example https://www.jmlr.org/)
        Output:
            - latest_paper_link: string (example https://www.jmlr.org/papers/volume25/23-1612/23-1612.pdf)
            - name_of_file: string (example 23-1612.pdf)
        """
        if self.check_and_create_folder():
            response = requests.get(url)  # Fetch the webpage
            
            if response.status_code == 200:  # Status code 200 means the request was successful
                soup = BeautifulSoup(response.text, 'html.parser')  # Create a BeautifulSoup object from the HTML code
                paper_links = soup.find_all('a', href=True)  # Find all links on the webpage
                
                pdf_links = [link['href'] for link in paper_links if link['href'].endswith('.pdf')]  # Find all links ending with .pdf
                
                if pdf_links:
                    latest_paper_link = pdf_links[0]
                    latest_paper_url = url + latest_paper_link
                    name_of_file = latest_paper_link.split('/')[-1]
                    return latest_paper_url, name_of_file    
                      
                else:
                    print("No PDF links found.")
                    return None, None
                
            else: 
                print(f"Error: {response.status_code}")
                return None, None
        
    def download_pdf(self, url: str, filename: str):
        """
        Downloads a PDF file from a URL and saves it locally.
        
        Input:
        - url: The URL of the PDF file
        - filename: The local filename to save the PDF as
        """
        try:    
            full_path = os.path.join('PDF_docs', filename)
            response = requests.get(url)
            if response.status_code == 200:
                with open(full_path, 'wb') as file:
                    file.write(response.content)
                print(f"Downloaded PDF and saved as {full_path}")

            else:
                print(f"Failed to download PDF. Status code: {response.status_code}")

        except Exception as e:
            print(f"An error occurred: {e}")

# Example usage:
bot = Paper_to_Chatbot()
url = 'https://www.jmlr.org/'  # Replace with the actual URL of the JMLR website
paper_url, filename = bot.getPaper(url)
if paper_url and filename:
    bot.download_pdf(paper_url, filename)



#     

# # Example usage:
# #download_pdf(str_latest_paper_link, '23-1612.pdf')


# def get_Abstract(url: str):
#     """
#     Eine Funktion, die das Abstract der Webseite https://www.jmlr.org/ abruft von der aktuellsten Veröffentlichung Paper
#     Input:
#         - url: string
#     Output:
#         - latest_paper_link: string
#     """
#     response = requests.get(url)                                    # Abrufen der Webseite
#     if response.status_code == 200:                                 # status code 200 bedeutet, dass die Anfrage erfolgreich war
#         text = response.text                                        # Inhalt der Webseite html code
#         soup = BeautifulSoup(text, 'html.parser')                   # Erstelle ein BeautifulSoup-Objekt form html code
#         paper_links = soup.find_all('a', href=True)                 # Finde alle Links auf der Webseite 
#         meta_data_ = [paper_link['href'] for paper_link in paper_links if paper_link['href'].endswith('.html')] # Finde alle Links die auf .html enden für die Abstract-Seite
        
#         ergebnis = [paper_link for paper_link in meta_data_ if '/papers/' in paper_link][0] # Wähle den Link der auf /papers/ endet
#         webpage_abs = url + ergebnis
#         return webpage_abs


# def get_Meta_Info(url: str):
#     """
#     Input
#     - url: URL of the JMLR website
#     Output
#     - meta_data: string with the Author, Title and Abstract and so on
#     """
#     response = requests.get(url)  # Abrufen der Webseite
    
#     if response.status_code == 200:  # Bei erfolgreichem Abrufen der Webseite
#         text = response.text  # Inhalt der Webseite HTML-Code
#         soup = BeautifulSoup(text, 'html.parser')  # Erstelle ein BeautifulSoup-Objekt vom HTML-Code
#         paper_links = soup.find_all('a', href=True)  # Finde alle Links auf der Webseite
#         meta_data_ = [link['href'] for link in paper_links if link['href'].endswith('.bib')]  # Finde alle Links, die auf .bib enden für die Metadaten
        
#         if not meta_data_:
#             return "No metadata link found."
        
#         meta_data = meta_data_[0]  # Wähle den aktuellsten Link
#         ergebnis_meta_info = url + meta_data
#         meta_information = requests.get(ergebnis_meta_info).text
        
#         title_match = re.search(r'title\s*=\s*\{(.+?)\}', meta_information, re.IGNORECASE)
#         author_match = re.search(r'author\s*=\s*\{(.+?)\}', meta_information, re.IGNORECASE)
        
#         title = title_match.group(1) if title_match else "Title not found"
#         author = author_match.group(1) if author_match else "Author not found"

#         result = "Title: '" + str(title) + "'" + " " + ", Author : " + "'" + str(author) + "'"

#         return result
#     else:
#         return f"Error: {response.status_code}"
   

# def text_splitter():
#     """
#     Initialisiert den Text-Splitter

#     Input:
#         - None

#     Output:
#         - text_splitter: Ein Objekt des Text-Splitters
#     """
    
#     text_splitter = RecursiveCharacterTextSplitter(
#         chunk_size=200,
#         chunk_overlap=50, 
#         length_function=len,
        
#     )

#     return text_splitter


# def PyPDFLoader_papers(pdf = str):
#     """
#     Initialisiert den WebBaseLoader

#     Input:
#         - None

#     Output:
#         - loader: Ein Objekt des WebBaseLoader
#     """
    
#     loader = PyPDFLoader(pdf)
#     pages = loader.load_and_split()
#     return pages


# def get_all_information(url:str):
#     """
#     Get all information from the website
#     """
    
#     paper_link = getPaper(url)
#     abstract_link = get_Abstract(url)
#     title, author = get_Meta_Info(url)
#     return paper_link, abstract_link, title, author


# def extract_text_from_pdf(filename: str):
#     """
#     Extracts text from a PDF file using PyMuPDF.
    
#     Input:
#     - filename: The local filename of the PDF
    
#     Output:
#     - text: Extracted text from the PDF
#     """
#     try:
#         document = fitz.open(filename)
#         text = ""
#         for page_num in range(document.page_count):
#             page = document.load_page(page_num)
#             text += page.get_text()
#         return text
#     except Exception as e:
#         return f"An error occurred: {e}"


# #extracted_text = extract_text_from_pdf(file_name)

        
# # Test the functions
# #str_latest_paper_link, latest_paper = getPaper('https://www.jmlr.org')

# #print(get_Meta_Info('https://www.jmlr.org'))
# #print(get_Abstract('https://www.jmlr.org'))
# #print(extract_title_and_author(get_Meta_Info('https://www.jmlr.org')))

# #print(get_all_information('https://www.jmlr.org'))