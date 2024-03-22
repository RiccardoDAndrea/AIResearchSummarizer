# Project Description

This project creates a chatbot using [Mistral](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2)  and [ChatGPT](https://python.langchain.com/docs/integrations/text_embedding/openai).

## Main Task

The main task is to start a virtual VM through Github Actions. This is executed by a cron job every day at 12 o'clock.

## Data Collection

To gather data for the chatbot, a web scraping function within a class is used to retrieve the latest scientific publications from [JMLR (Journal of Machine Learning Research)](https://www.jmlr.org/). This involves extracting the abstract of the journal as well as the metadata of the paper, including author and title.

## Chatbot Initialization

Once the data is collected, a chatbot is initialized. This involves using Mistral Mistral-7B-Instruct-v0.2 and ChatGPT 3.5 Turbo. An RAG system is utilized to provide the chatbots with the abstract and metadata of the paper.

## Functionality

The chatbots are then instructed to return the authors, title, and key findings from the abstract.

