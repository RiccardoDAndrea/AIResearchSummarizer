
from langchain_openai import ChatOpenAI
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.chains import RetrievalQAWithSourcesChain


# Stategie:
## Als class ein OpenAI llm Bauen, dass die Frage beantwortet. 
## Gefolgt von einer automatiesierten möglichkeit Daten (PDFs) zu extrahieren und zu verarbeiten. 
## - WO : /Users/riccardo/Desktop/Repositorys_Github/LLM/Docs/docs_for_llm_pipline
## Eine große merged PDF dokumente, dass die Daten enthält.
## Und zu letzt ein Github action skript ausführen das die Pdfs automatischt zusammen fließen lässt 
##
##


# Öffne die JSON-Datei und lade den Inhalt
with open('/Users/riccardo/Desktop/Repositorys_Github/LLM/Docs/api_token.json', 'r') as api_file:
    api_token_file = json.load(api_file)
    open_ai_token = api_token_file['Open_api_token']

# Extrahiere die Variable aus den Daten


class OpenAI_RAG:
    def __init__(self, open_ai_token: str):
        self.open_ai_token = open_ai_token

    def text_splitter(self):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=200,
            chunk_overlap=50, 
            length_function=len
        )
        return text_splitter

    def loader_for_chunks(self, text_splitter):
        filepath = '/Users/riccardo/Desktop/Repositorys_Github/LLM/Docs/merged.pdf'
        loader = PyPDFLoader(filepath)
        chunks = loader.load_and_split(text_splitter=text_splitter)
        return chunks

    def embedding(self):
        embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        return embedding_function

    def initialise_chroma(self, chunks, embedding_function):
        db = Chroma.from_documents(chunks, embedding_function)
        return db
    
    def retriever(self, db, query):
        retriever = db.as_retriever()
        retriever.get_relevant_documents(query)
        return retriever

    def llm_model(self):
        llm = ChatOpenAI(
            openai_api_key= self.open_ai_token,
            model_name = "gpt-3.5-turbo",
            temperature = 0.0,
            max_tokens = 150
        )
        return llm
        
    def qa_with_sources(self, query):
        llm = self.llm_model()
        text_splitter_instance = self.text_splitter()
        chunks = self.loader_for_chunks(text_splitter_instance)
        embedding_instance = self.embedding()
        retriever_instance = self.retriever(Chroma.from_documents(chunks, embedding_instance), query)
        qa_with_sources = RetrievalQAWithSourcesChain.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever_instance)
        return qa_with_sources(query)

# Erstelle eine Instanz der Klasse OpenAI_RAG
openai_rag = OpenAI_RAG(open_ai_token)

# Stelle eine Frage und erhalte die Antwort
query = "Can you summarize the Abstract in the paper 'Attention Is All You Need?'"
antwort = openai_rag.qa_with_sources(query)

# Gib die Antwort aus
print("Antwort:", antwort)































### text_splitter = RecursiveCharacterTextSplitter(
### chunk_size=200,
### chunk_overlap=50, 
### length_function = len)

### filepath = '/Users/riccardo/Desktop/Repositorys_Github/LLM/Docs/merged.pdf'
### loader = PyPDFLoader(filepath)
### chunks = loader.load_and_split(text_splitter=text_splitter)

# for chunk in chunks[:29]:
#     print("Page content: \n", chunk.page_content),
#     print("Page_metadata: \n", chunk.metadata),
#     print("----------------------------")
# embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
# embedding = embedding_function.embed_documents("This is a test sentence.")

# # print(embedding[0])
# # print("Dimension of Embedding: ", len(embedding[0]))
# db = Chroma.from_documents(chunks, embedding_function)
# #print("Chunks in DB:", db._collection.count())
# query = "Give me the first chapter name."
# retriever = db.as_retriever()
# retriever.get_relevant_documents(query)


# llm = ChatOpenAI(
#     openai_api_key= open_ai_token,
#     model_name = "gpt-3.5-turbo",
#     temperature = 0.0,
#     max_tokens = 100
#     )


# qa_with_sources = RetrievalQAWithSourcesChain.from_chain_type(
#     llm = llm,
#     chain_type = "stuff",  
#     retriever = retriever
#     )
# qa_with_sources

