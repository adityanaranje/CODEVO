---
title: Cod Evo
emoji: 🚀
colorFrom: red
colorTo: red
sdk: streamlit
app_port: 8501
tags:
- streamlit
pinned: false
short_description: Streamlit template space
---

# Advanced GitHub Repository RAG Q&A Bot

A sophisticated Retrieval-Augmented Generation (RAG) system that analyzes GitHub repositories, generate code and answers questions using Groq LLM, FAISS vector store, and HuggingFace embeddings.

## Features

- **Smart Repository Crawling**: Automatically processes various file types (Python, JavaScript, Java, C++, documentation, etc.)
- **Language-Aware Processing**: Uses different text splitters based on file types
- **Fast LLM Inference**: Powered by Groq for quick and accurate responses
- **Efficient Vector Search**: FAISS for fast similarity search
- **Rich Source Attribution**: Shows exactly which files and code sections were used to answer questions
- **Repository Analysis**: Automated analysis of project structure and components

## File Structure

```
├── config.py              # Configuration and API keys
├── github_repository.py   # GitHub API handling and repository crawling
├── document_processor.py  # Document chunking and processing
├── embedding_manager.py   # FAISS vector store and embeddings
├── llm_manager.py         # Groq LLM integration for github repo
├── code_generate.py       # Groq LLM for code generation
├── rag_system.py          # Main RAG pipeline orchestration
├── main.py               # Streamlit web application
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

Edit `config.py` and replace the placeholder values:

```python
@dataclass
class Config:
    GROQ_API_KEY: str = "your_actual_groq_api_key_here"  # Get from https://console.groq.com/
    GITHUB_TOKEN: str = "your_actual_github_token_here"  # Optional but recommended
    # ... other settings
```

**Getting API Keys:**
- **Groq API Key**: Sign up at [https://console.groq.com/](https://console.groq.com/) and generate an API key
- **GitHub Token**: Go to GitHub Settings > Developer settings > Personal access tokens > Generate new token (classic). Only needs public repository read access.

### 3. Run the Application

```bash
streamlit run main.py
```

The application will open in your web browser at `http://localhost:8501`

## Usage

1. **Enter Repository URL**: Paste a GitHub repository URL in the sidebar (e.g., `https://github.com/langchain-ai/langchain`)

2. **Process Repository**: Click "Process Repository" to crawl and analyze the repository. This may take a few minutes for large repositories.

3. **Ask Questions**: Once processing is complete, ask questions about the repository:
   - "How does the authentication work?"
   - "What are the main components?"
   - "How do I install and set up this project?"
   - "What testing frameworks are used?"

4. **View Sources**: Each answer shows the specific files and code sections that were used to generate the response.



## Architecture

### Core Components

- **GitHubRepository**: Handles GitHub API interactions, file filtering, and repository crawling
- **AdvancedDocumentProcessor**: Applies language-specific text splitting for optimal chunking
- **EmbeddingManager**: Manages HuggingFace embeddings and FAISS vector store
- **LLMManager**: Interfaces with Groq LLM for response generation
- **AdvancedRAGSystem**: Orchestrates the entire RAG pipeline

### RAG Pipeline

1. **Repository Crawling**: Fetches files from GitHub API with intelligent filtering
2. **Document Processing**: Splits documents using language-aware strategies
3. **Embedding Creation**: Generates embeddings using HuggingFace models
4. **Vector Storage**: Stores embeddings in FAISS for efficient similarity search
5. **Query Processing**: Retrieves relevant chunks and generates responses using Groq

## Supported File Types

- **Programming Languages**: Python, JavaScript/TypeScript, Java, C/C++, C#, PHP, Ruby, Go, Rust, Scala, Kotlin
- **Documentation**: Markdown, reStructuredText, Plain Text
- **Configuration**: JSON, YAML, TOML, INI
- **Web Technologies**: HTML, CSS, SCSS
- **Special Files**: README, LICENSE, CHANGELOG, DOCKERFILE, MAKEFILE

## Configuration Options

Edit `config.py` to customize:

- `CHUNK_SIZE`: Size of text chunks for processing (default: 1000)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 200)
- `TOP_K_RETRIEVAL`: Number of relevant chunks to retrieve (default: 5)
- `TEMPERATURE`: LLM response randomness (default: 0.3)
- `MAX_TOKENS`: Maximum response length (default: 2048)

## Troubleshooting

### Common Issues

1. **API Key Errors**: Ensure your Groq API key is valid and active in `config.py`
2. **Repository Access**: Some repositories may be private or have restrictions
3. **Large Repositories**: May take longer to process and require more memory
4. **Rate Limits**: GitHub token helps avoid API rate limits

### Performance Tips

- Use GitHub tokens for better API rate limits
- Process smaller repositories first to test setup
- Groq provides fast inference compared to local models
- FAISS ensures efficient similarity search even for large repositories

## Dependencies

- **streamlit**: Web interface
- **langchain**: Document processing and text splitting
- **groq**: LLM inference
- **sentence-transformers**: Embeddings
- **faiss-cpu**: Vector similarity search
- **requests**: GitHub API calls
