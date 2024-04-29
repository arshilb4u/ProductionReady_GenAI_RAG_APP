import gradio as gr
from typing import List,Tuple
import os
from utils.Config import LoadConfig
from langchain.vectorstores import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
import time

config = LoadConfig()
llm= ChatOpenAI()
embeddings = OpenAIEmbeddings()

class Chat:
    @staticmethod
    
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    @staticmethod
    def RetrieveContent(
            chatcontent : List,
            usersmessages :str,
            Process_type : str = "Preprocessed doc") -> Tuple:
        print(chatcontent,usersmessages,Process_type)
        if Process_type=="Preprocessed doc":
            if os.path.exists(config.persist_directory):
                vectordb =  Chroma(persist_directory = config.persist_directory,
                                   embedding_function = embeddings)
            else :
                chatcontent.append((usersmessages,"DataBase is not available please connect to Admin Arshil Singh Bhatia or try uploading files to chat with it "))
                return " ", chatcontent, None

        elif Process_type == "Upload doc: Process for RAG":
            if os.path.exists(config.customer_persist_directory):
                vectordb =  Chroma(persist_directory = config.customer_persist_directory,
                                   embedding_function =embeddings)
                
            else:
                chatcontent.append((usersmessages,"File was not uploaded please upload the file and try again. Please connect with Admin Arshil Singh Bhatia in case of any issue"))
                return " ", chatcontent, None

        retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k":config.k })
        chat_history = f"Chat history:\n {str(chatcontent[-config.number_of_q_a_pairs:])}\n\n"
        print(retriever,chat_history)
        custom_rag_prompt = PromptTemplate.from_template(config.llm_system_role)
        print(custom_rag_prompt)
        rag_chain = (
        {"context": retriever | Chat.format_docs, "question": RunnablePassthrough()}
        | custom_rag_prompt
        | llm
        | StrOutputParser()
        )
        print(rag_chain.invoke(usersmessages))

        chatcontent.append((usersmessages, rag_chain.invoke(usersmessages)))
        time.sleep(2)
        return "", chatcontent
        



