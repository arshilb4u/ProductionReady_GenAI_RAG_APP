import yaml
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from typing import Tuple, List
from utils.Config import LoadConfig
from pyprojroot import here
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import re
import ast
import html
import os
from openai import OpenAI

llm= ChatOpenAI()


config = LoadConfig()

embeddings = OpenAIEmbeddings()

vectordb = Chroma(persist_directory= config.persist_directory,
                  embedding_function = embeddings)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

while True:
    question = input("\n\n Please enter your question, or enter 'q' to EXIT")
    if question.lower() == 'q':
        break
    retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k":config.k })
    custom_rag_prompt = PromptTemplate.from_template(config.llm_system_role)
    rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | custom_rag_prompt
    | llm
    | StrOutputParser()
)

    print(rag_chain.invoke(question))
