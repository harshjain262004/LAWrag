from textToVector import *
from db import *
import os
from pathlib import Path

pdf_folder = Path("pdfs")

def main():
    def extract_text_from_pdf(pdf_file):
        from langchain_community.document_loaders import PyMuPDFLoader
        from langchain.text_splitter import RecursiveCharacterTextSplitter

        loader = PyMuPDFLoader(pdf_file)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        texts = text_splitter.split_documents(documents)
        ChunksArr = [text.page_content for text in texts]
        return ChunksArr

    for pdf_file in pdf_folder.glob("*.pdf"):
        print(pdf_file.name)
        ChunksArr = extract_text_from_pdf(pdf_file)
        embeddingArr = getEmbeddings(ChunksArr)
        addVectors(ChunksArr,embeddingArr,pdf_file.name)

# main()