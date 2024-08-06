# Example usage
# if __name__ == "__main__":
#     url = "https://www.jmlr.org/"
#     query = "What is the latest paper about?"
#     paper_to_chatbot = Paper_to_Chatbot(url)
#     latest_paper_url, filename = paper_to_chatbot.getPaper()
#     if latest_paper_url and filename:
#         paper_to_chatbot.download_pdf(latest_paper_url, filename)
#     documents = paper_to_chatbot.retriever(query)
#     if documents:
#         for doc in documents:
#             print(doc)