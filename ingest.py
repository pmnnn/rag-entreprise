from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_voyageai import VoyageAIEmbeddings
import os

# Charge la clé API depuis .env
load_dotenv()

def ingest_documents():
    # ÉTAPE 1 — Lire les PDF
    print("📂 Chargement des PDF...")
    loader = PyPDFDirectoryLoader("data/")
    documents = loader.load()
    print(f"✅ {len(documents)} pages chargées")

    # ÉTAPE 2 — Découper en chunks
    print("✂️  Découpage en chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,      # taille max d'un chunk (en caractères)
        chunk_overlap=200,    # chevauchement entre chunks
    )
    chunks = splitter.split_documents(documents)
    print(f"✅ {len(chunks)} chunks créés")

    # ÉTAPE 3 — Stocker dans ChromaDB
    embeddings = VoyageAIEmbeddings(
    model="voyage-3",
    voyage_api_key=os.getenv("VOYAGE_API_KEY")
    )
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="chroma_db"
    )
    print(f"✅ Base vectorielle créée dans chroma_db/")
    print("🎉 Ingestion terminée !")

if __name__ == "__main__":
    ingest_documents()

    