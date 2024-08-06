    def getAbstract(self):
        """
        Eine Funktion, die das Abstract der Webseite https://www.jmlr.org/ abruft von der aktuellsten Veröffentlichung Paper
        Input:
            - url: string
        Output:
            - abstract: string
        """
        response = requests.get(self.url)  # Abrufen der Webseite
        if response.status_code == 200:  # status code 200 bedeutet, dass die Anfrage erfolgreich war
            text = response.text  # Inhalt der Webseite html code
            soup = BeautifulSoup(text, 'html.parser')  # Erstelle ein BeautifulSoup-Objekt form html code
            paper_links = soup.find_all('a', href=True)  # Finde alle Links auf der Webseite 
            # Finde alle Links die auf .html enden für die Abstract-Seite
            meta_data_ = [paper_link['href'] for paper_link in paper_links if paper_link['href'].endswith('.html')] 
            
            ergebnis = [paper_link for paper_link in meta_data_ if '/papers/' in paper_link][0]  # Wähle den Link der auf /papers/ endet
            abstract_url = self.url + ergebnis
            response = requests.get(abstract_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                abstract = soup.find('div', {'class': 'abstract'}).text.strip()
                abstract = abstract.replace('\n', ' ')
                print(abstract)
                return abstract
            else:
                print(f"Error fetching abstract page: {response.status_code}")
                return None
        else:
            print(f"Error: {response.status_code}")
            return None