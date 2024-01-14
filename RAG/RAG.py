from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain.schema.runnable import RunnablePassthrough
import csv
from loadPDF import loadPDF

PDFname = loadPDF()

loader = PyPDFLoader(PDFname)        

#from https://python.langchain.com/docs/use_cases/question_answering/
        
# Split documents
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
splits = text_splitter.split_documents(loader.load())

# Embed and store splits
vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
retriever = vectorstore.as_retriever()

# Prompt
# https://smith.langchain.com/hub/rlm/rag-prompt

rag_prompt = hub.pull("rlm/rag-prompt")

# LLM

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

# RAG chain 

rag_chain = {"context": retriever, "question": RunnablePassthrough()} | rag_prompt | llm

again = True

while (again):

    question = input("What's your question? Type q to quit: ")

    if (question == 'q'):
        again = False
        break
            
    result = rag_chain.invoke(question)

    print(result)