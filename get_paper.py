import requests
from bs4 import BeautifulSoup

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
            #print(str_latest_paper_link)
            return str_latest_paper_link

    return None

def update_pdf_links(url: str, pdf_links: set):
    """
    Eine Funktion, die die PDF-Links-Liste aktualisiert, indem sie neue Links hinzufügt und doppelte entfernt.
    Input:
        - url: string
        - pdf_links: set
    Output:
        - updated_pdf_links: set
    """
    new_link = getPaper(url)
    if new_link:
        pdf_links.add(new_link)
    return pdf_links

# Initialisiere ein Set für die PDF-Links
str_latest_paper_link = set()

# Update die PDF-Links-Liste
pdf_paper_links_set = update_pdf_links('https://www.jmlr.org/', str_latest_paper_link)
str_pdf_paper_links_set = ''.join(pdf_paper_links_set)
print(str_pdf_paper_links_set)
