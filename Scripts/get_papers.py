import requests
from bs4 import BeautifulSoup
import bibtexparser
def getMeta_data(url):
    """
    Get the meta of the webpage https://www.jmlr.org/papers/v25/
    From last paper that was published we retrieve Author and Title

    Input:
        - url: string
    Output:
        - author: string
        - title: string
    """
    response = requests.get(url)
    if response.status_code == 200:
        text = response.text
    soup = BeautifulSoup(text, 'html.parser')
    paper_links = soup.find_all('a', href=True)
    meta_data_ = [link['href'] for link in paper_links if link['href'].endswith('.bib')]
    meta_data = meta_data_[-1]
    last_meta_data = requests.get(url + meta_data)
    text_meta_data = last_meta_data.text
    # # Parse den Inhalt der .bib-Datei
    bib_database = bibtexparser.loads(text_meta_data)

    # # Extrahiere Autor und Titel des ersten Eintrags
    first_entry = bib_database.entries[0]

    author, title= first_entry['author'], first_entry['title']

    return author, title 

author, title  = getMeta_data('https://www.jmlr.org')

#print("Autor:", author)
#print("Titel:", title)


def getAbstract(url):
    response = requests.get(url)
    if response.status_code == 200:
        text = response.text
        soup = BeautifulSoup(text, 'html.parser')
        paper_links = soup.find_all('a', href=True)
        meta_data_ = [paper_link['href'] for paper_link in paper_links if paper_link['href'].endswith('.html')]
        ergebnis = [paper_link for paper_link in meta_data_ if '/papers/' in paper_link]
        #print(url + ergebnis[0])
        response_for_Abstract = requests.get(url + ergebnis[0])
        if response_for_Abstract.status_code == 200:
            text = response_for_Abstract.text
            soup_abstract = BeautifulSoup(text, 'html.parser')  # Verwende ein neues BeautifulSoup-Objekt für die Abstract-Seite
            abstract_text = soup_abstract.find('p', class_='abstract')
            if abstract_text:  # Überprüfe, ob das Abstract-Element gefunden wurde
                abstract = print(abstract_text.get_text(strip=True))
            else:
                print("Abstract nicht gefunden.")
                return abstract



Abstract = getAbstract('https://www.jmlr.org')
Abstract
#author, title  = getMeta_data('https://www.jmlr.org')
