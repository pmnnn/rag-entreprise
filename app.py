import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_voyageai import VoyageAIEmbeddings
from langchain_chroma import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
import os
import json
from datetime import datetime
from pathlib import Path

load_dotenv()

HISTORY_FILE = "conversation_history.json"

# ─── Fonctions pour gérer l'historique ───

def load_all_conversations():
    if Path(HISTORY_FILE).exists():
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_all_conversations(conversations):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(conversations, f, ensure_ascii=False, indent=2)

def get_conversation_title(messages):
    for msg in messages:
        if msg["role"] == "user":
            title = msg["content"][:40]
            return title + "..." if len(msg["content"]) > 40 else title
    return "Nouvelle conversation"

# ─── Configuration de la page ───

st.set_page_config(
    page_title="RAG Entreprise",
    page_icon="📚",
    layout="wide"
)

# ─── Initialisation de l'état ───

if "conversations" not in st.session_state:
    st.session_state.conversations = load_all_conversations()

if "current_id" not in st.session_state:
    new_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.session_state.current_id = new_id
    st.session_state.conversations[new_id] = []
    save_all_conversations(st.session_state.conversations)

if "messages" not in st.session_state:
    current_id = st.session_state.current_id
    st.session_state.messages = st.session_state.conversations.get(current_id, [])

# ─── Sidebar ───

with st.sidebar:
    st.markdown("## RAG Entreprise")
    st.divider()

    if st.button("Nouvelle conversation", use_container_width=True):
        new_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        st.session_state.current_id = new_id
        st.session_state.conversations[new_id] = []
        st.session_state.messages = []
        save_all_conversations(st.session_state.conversations)
        st.rerun()

    st.markdown("### Conversations")

    for conv_id, messages in reversed(list(st.session_state.conversations.items())):
        if not messages:
            title = "Nouvelle conversation"
        else:
            title = get_conversation_title(messages)

        is_active = conv_id == st.session_state.current_id
        label = f">> {title}" if is_active else title

        col1, col2 = st.columns([5, 1])
        with col1:
            if st.button(label, key=f"conv_{conv_id}", use_container_width=True):
                st.session_state.current_id = conv_id
                st.session_state.messages = st.session_state.conversations[conv_id]
                st.rerun()
        with col2:
            if st.button("x", key=f"del_{conv_id}"):
                del st.session_state.conversations[conv_id]
                save_all_conversations(st.session_state.conversations)
                if conv_id == st.session_state.current_id:
                    new_id = datetime.now().strftime("%Y%m%d_%H%M%S")
                    st.session_state.current_id = new_id
                    st.session_state.conversations[new_id] = []
                    st.session_state.messages = []
                st.rerun()

# ─── Chargement du RAG ───

@st.cache_resource
def load_chain():
    embeddings = VoyageAIEmbeddings(
        model="voyage-3",
        voyage_api_key=os.getenv("VOYAGE_API_KEY")
    )
    vectordb = Chroma(
        persist_directory="chroma_db",
        embedding_function=embeddings
    )
    retriever = vectordb.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0
    )
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"
    )
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True,
    )
    return chain

chain = load_chain()

# ─── Interface principale ───

st.title("Assistant Documentaire Interne")
st.caption("Posez vos questions — je réponds en citant vos documents.")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if question := st.chat_input("Posez votre question sur la documentation..."):

    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Recherche dans les documents..."):
            result = chain({"question": question})
            answer = result["answer"]
            sources = result["source_documents"]

        st.markdown(answer)

        if sources:
            with st.expander(f"Sources ({len(sources)} extraits)"):
                for i, doc in enumerate(sources, 1):
                    meta = doc.metadata
                    st.markdown(f"**Source {i}** — `{meta.get('source', 'Inconnu')}` "
                                f"(page {meta.get('page', '?')})")
                    st.markdown(f"> {doc.page_content[:300]}...")
                    st.divider()

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.session_state.conversations[st.session_state.current_id] = st.session_state.messages
    save_all_conversations(st.session_state.conversations)