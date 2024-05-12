from bs4 import BeautifulSoup
import requests
### The following script is used to get the unique link of the paper
### That include the meta information and the abstract links.
### The script is used to get the unique link of the paper


response = requests.get("https://www.jmlr.org")      
                      
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


print(ergebnis_meta_info)
print(webpage_abs)