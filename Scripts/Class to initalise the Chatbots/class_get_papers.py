import requests
from bs4 import BeautifulSoup
import bibtexparser

### Der folgende Skirpt wird verwendet, um die Metadaten und das Abstract der 
### neuesten Veröffentlichung von JMLR abzurufen.
### Als variable erhaöten wir den Autor, den Titel und das Abstract der neuesten Veröffentlichung

class getPapers:
    """
    Eine Klasse für unseren LLM der mit einer RAG Modell ausgesatet wird.
    Und die neusten Papers von JMLR abruft.
    
    """
    def getMeta_data(self, url:str): 
        """

        Abrufen der Metadaten der Webseite https://www.jmlr.org/
        Von der akutellsten veröffentlichung Arbeit werden Autor und Titel abgerufen

        Input:
            - url: string

        Output:
            - author: string
            - title: string

        """
        response = requests.get(url)   
        
        if response.status_code == 200:                                     # bei erfolgreich abrufen der Webseite
            text = response.text                                            # Inhalt der Webseite html code
            soup = BeautifulSoup(text, 'html.parser')                       # Erstelle ein BeautifulSoup-Objekt form html code
            paper_links = soup.find_all('a', href=True)                     # Finde alle Links auf der Webseite
            meta_data_ = [link['href'] for link in paper_links if link['href'].endswith('.bib')] # Finde alle Links die auf .bib enden für die Metadaten
            meta_data = meta_data_[0]                                       # Wähle den akutellsten Link
            last_meta_data = requests.get(url + meta_data)
            
            if last_meta_data.status_code == 200:
                text_meta_data = last_meta_data.text                        # Inhalt der .bib-Datei die Akutelle internet seite
                # Parse den Inhalt der .bib-Datei
                bib_database = bibtexparser.loads(text_meta_data)

                # Extrahiere Autor und Titel des ersten Eintrags
                first_entry = bib_database.entries[0]                       # ein dict mit allen werten die wir im nächsten schritt extrahieren

                author, title = first_entry['author'], first_entry['title'] # Extrahiere Autor und Titel

        return author, title 

    def getAbstract(self, url:str):  
        """
        Eine funktion die das Abstract der Webseite https://www.jmlr.org/ abruft von der aktuellsten veröffentlichung Paper
        Input:
            - url: string
        Output:
            - abstract_text: string
        
        """
        response = requests.get(url)                                    # Abrufen der Webseite
        if response.status_code == 200:                                 # status code 200 bedeutet, dass die Anfrage erfolgreich war
            text = response.text                                        # Inhalt der Webseite html code
            soup = BeautifulSoup(text, 'html.parser')                   # Erstelle ein BeautifulSoup-Objekt form html code
            paper_links = soup.find_all('a', href=True)                 # Finde alle Links auf der Webseite 
            meta_data_ = [paper_link['href'] for paper_link in paper_links if paper_link['href'].endswith('.html')] # Finde alle Links die auf .html enden für die Abstract-Seite
            
            ergebnis = [paper_link for paper_link in meta_data_ if '/papers/' in paper_link] # Wähle den Link der auf /papers/ endet
            
            if ergebnis:
                response_for_Abstract = requests.get(url + ergebnis[0]) # Abrufen der Abstract-Seite
                
                if response_for_Abstract.status_code == 200:            # Wenn Seite erfolgreich abgerufen wurde
                    text = response_for_Abstract.text                   # Inhalt der Abstract-Seite html code
                    soup_abstract = BeautifulSoup(text, 'html.parser')  # Verwende ein neues BeautifulSoup-Objekt für die Abstract-Seite
                    abstract_text = soup_abstract.find('p', class_='abstract') # Finde das Abstract-Element
                    
                    if abstract_text:                                   # Überprüfe, ob das Abstract-Element gefunden wurde
                        abstract_text = abstract_text.get_text(strip=True) 
                        return abstract_text       # Gebe das Abstract zurück
                    
                    else:
                        print("Abstract nicht gefunden.")
            
            else:
                print("Kein Abstract-Link gefunden.")
            return None
                
    def initialize(self, url):
        author, title = self.getMeta_data(url)                          # Extrahiere Autor und Titel
        abstract = self.getAbstract(url)                                # Extrahiere Abstract
        return author, title, abstract
        
#Instanziiere die Klasse
get_papers = getPapers()

author, title, abstract = get_papers.initialize('https://www.jmlr.org')


print(f"Author: {author}\nTitle: {title}\nAbstract: {abstract}")




    
