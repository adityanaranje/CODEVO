# 🚀 Advanced GitHub Repository RAG Q&A & Code Generation Bot

A sophisticated **Retrieval-Augmented Generation (RAG)** system that analyzes GitHub repositories, generates code, and answers questions using **Groq LLM**, **FAISS vector store**, and **HuggingFace embeddings**.

---

### 🌐 Try It Here [Live](https://codevo-aditya.streamlit.app/)

---
## ✨ Features

- **📂 Smart Repository Crawling**: Automatically processes multiple file types (Python, JavaScript, Java, C++, docs, etc.)  
- **🧠 Language-Aware Processing**: Uses different text splitters based on file types for optimal chunking  
- **⚡ Fast LLM Inference**: Powered by Groq for quick and accurate responses  
- **🔍 Efficient Vector Search**: FAISS for lightning-fast similarity search  
- **📝 Rich Source Attribution**: Shows exactly which files and code sections were used to answer questions  
- **🧩 Repository Analysis**: Automated analysis of project structure and components  
- **💻 Code Generation**: Generate code snippets or functions using Groq LLM prompt templates  

---

## 📁 File Structure

```
├── config.py              # Configuration and API keys
├── github_repository.py   # GitHub API handling and repository crawling
├── document_processor.py  # Document chunking and processing
├── embedding_manager.py   # FAISS vector store and embeddings
├── llm_manager.py         # Groq LLM integration for GitHub repo
├── code_generate.py       # Groq LLM for code generation using prompt templates
├── rag_system.py          # Main RAG pipeline orchestration
├── main.py                # Streamlit web application
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

---

## ⚙️ Setup Instructions

### 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Configure API Keys

Edit `config.py` and replace the placeholder values:

```python
@dataclass
class Config:
    GROQ_API_KEY: str = "your_actual_groq_api_key_here"  # Get from https://console.groq.com/
    GITHUB_TOKEN: str = "your_actual_github_token_here"  # Optional but recommended
    # ... other settings
```

**Getting API Keys:**
- **🔑 Groq API Key**: [Sign up here](https://console.groq.com/) and generate an API key  
- **🐙 GitHub Token**: GitHub Settings → Developer Settings → Personal Access Tokens → Generate new token (classic). Only requires public repo read access  

### 3️⃣ Run the Application

```bash
streamlit run main.py
```

The app will open in your browser at `http://localhost:8501`

---

## 📝 Usage

1. **Enter Repository URL**: Paste a GitHub repo URL in the sidebar (e.g., `https://github.com/langchain-ai/langchain`)  
2. **Process Repository**: Click **"Process Repository"** to crawl and analyze the repo. (May take a few minutes for large repos)  
3. **Ask Questions**: Once processed, ask questions like:  
   - "How does authentication work?"  
   - "What are the main components?"  
   - "How do I set up this project?"  
   - "Which testing frameworks are used?"  
4. **Generate Code**: Use the **Code Generation** tab to create functions, scripts, or snippets using Groq LLM prompt templates  
5. **View Sources**: Each answer shows the specific files and code sections that were used to generate the response  

---

## 🏗 Architecture

### Core Components

- **GitHubRepository**: Handles GitHub API interactions, file filtering, and crawling  
- **AdvancedDocumentProcessor**: Applies language-specific text splitting  
- **EmbeddingManager**: Manages HuggingFace embeddings and FAISS vector store  
- **LLMManager**: Interfaces with Groq LLM for responses  
- **AdvancedRAGSystem**: Orchestrates the RAG pipeline  
- **CodeGenerator**: Generates code based on Groq LLM prompt templates  

### RAG + Code Generation Pipeline

1. **Repository Crawling**: Fetches files with intelligent filtering  
2. **Document Processing**: Splits documents using language-aware strategies  
3. **Embedding Creation**: Generates embeddings via HuggingFace  
4. **Vector Storage**: Stores embeddings in FAISS for similarity search  
5. **Query Processing**: Retrieves relevant chunks and generates responses using Groq  
6. **Code Generation**: Uses prompt templates to generate code snippets or functions  

---

## 🗂 Supported File Types

- **Programming Languages**: Python, JavaScript/TypeScript, Java, C/C++, C#, PHP, Ruby, Go, Rust, Scala, Kotlin  
- **Documentation**: Markdown, reStructuredText, Plain Text  
- **Configuration**: JSON, YAML, TOML, INI  
- **Web**: HTML, CSS, SCSS  
- **Special Files**: README, LICENSE, CHANGELOG, DOCKERFILE, MAKEFILE  

---

## ⚙️ Configuration Options (`config.py`)

- `CHUNK_SIZE`: Size of text chunks (default: 1000)  
- `CHUNK_OVERLAP`: Overlap between chunks (default: 200)  
- `TOP_K_RETRIEVAL`: Number of relevant chunks to retrieve (default: 5)  
- `TEMPERATURE`: LLM response randomness (default: 0.3)  
- `MAX_TOKENS`: Maximum response length (default: 2048)  

---

## ⚠️ Troubleshooting

### Common Issues

1. **API Key Errors**: Ensure Groq API key is valid in `config.py`  
2. **Repository Access**: Some repos may be private or restricted  
3. **Large Repositories**: May take longer and require more memory  
4. **Rate Limits**: Using a GitHub token avoids hitting API limits  

### Performance Tips

- Use GitHub tokens for better API rate limits  
- Test on smaller repos first  
- Groq provides fast inference  
- FAISS ensures efficient similarity search  

---

## 🖼 RAG + Code Generation Pipeline

```text
                 🌐 GitHub Repository
                          │
                          ▼
                📂 Repository Crawling                                     💻 Code Generation
        (GitHub API fetch + file filtering)                             (Prompt templates with Groq)
                          │                                                          │
                          ▼                                                          |
              Advanced Document Processing                                           │
       (Language-aware chunking & preprocessing)                                     │
                          │                                                          |
                          ▼                                                          ▼                                     
             Embedding Creation (HuggingFace)                                     User Input
                          │                                                  (Get query from user)   
                          ▼                                                          |        
              Vector Storage (FAISS Indexing)                                        |
                          │                                                          |
                          |                                                          │
                          ▼                                                          |
                Query Processing (RAG Q&A)                               🛠 Generated Code Snippets   
                (Retrieve relevant chunks)                            (Functions, scripts, examples)
                          │                                                          |
                          ▼                                                          | 
               LLM Response Generation                                               |
              (Groq LLM answers questions)                                           |
                          │                                                          |
                           ────────────>✅ User Interface (Streamlit)✅<────────────
```

**Legend / Highlights:**
- 🌐 Source GitHub repo  
- 📂 Crawling & filtering  
- 🧠 Language-specific processing  
- 🔗 Embeddings creation for semantic search  
- 📊 FAISS for fast retrieval  
- 📖 Q&A for GitHub knowledge  
- 💻 Code Generation using Groq LLM prompt templates  
- ✅ Streamlit interface for easy access  

---

## 📦 Dependencies

- **streamlit**: Web interface  
- **langchain**: Document processing & splitting  
- **groq**: LLM inference  
- **sentence-transformers**: Embeddings  
- **faiss-cpu**: Vector similarity search  
- **requests**: GitHub API calls  

---

✅ Now, you can **explore repositories, ask questions, and even generate code** all in one place!

