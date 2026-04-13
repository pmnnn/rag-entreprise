# RAG d'Entreprise

Un chatbot intelligent qui répond aux questions sur vos documents internes (PDF) en citant la source exacte — fichier et numéro de page.

## Le problème résolu
Les employés perdent 20% de leur temps à chercher des informations dans la documentation interne. Ce projet permet de poser des questions en langage naturel et d'obtenir une réponse instantanée avec la source exacte.

## Fonctionnalités
- Ingestion de PDF automatique
- Recherche sémantique (comprend le sens, pas juste les mots exacts)
- Historique des conversations persistant
- Citation des sources avec nom du fichier et numéro de page
- Interface web intuitive

## Stack technique
- **LLM** : Claude Haiku (Anthropic)
- **Embeddings** : Voyage-3 (Voyage AI)
- **VectorDB** : ChromaDB (local)
- **Framework** : LangChain
- **Interface** : Streamlit

## Installation

### 1. Clone le projet
```bash
git clone https://github.com/ton-username/rag-entreprise.git
cd rag-entreprise
```

### 2. Crée l'environnement virtuel
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Installe les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configure les clés API
Crée un fichier `.env` à la racine :
```
ANTHROPIC_API_KEY=ta-clé-anthropic
VOYAGE_API_KEY=ta-clé-voyage
```

Clé Anthropic : [console.anthropic.com](https://console.anthropic.com)
Clé Voyage AI : [dash.voyageai.com](https://dash.voyageai.com)

### 5. Ajoute tes PDF
Copie tes documents PDF dans le dossier `data/`

### 6. Lance l'ingestion
```bash
python ingest.py
```

### 7. Lance l'application
```bash
streamlit run app.py
```

L'interface s'ouvre automatiquement sur `http://localhost:8501`

## Structure du projet
```
rag-entreprise/
├── data/                    # Tes documents PDF
├── chroma_db/               # Base vectorielle (générée automatiquement)
├── ingest.py                # Script d'ingestion des PDF
├── app.py                   # Interface web Streamlit
├── requirements.txt         # Dépendances Python
├── .env                     # Clés API (jamais sur GitHub !)
└── .gitignore
```