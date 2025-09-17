from dataclasses import dataclass
from dotenv import load_dotenv
import os
load_dotenv()

@dataclass
class Config:
    GROQ_API_KEY: str = st.secrets["GROQ_API_KEY"]  # Replace with your actual Groq API key
    GITHUB_TOKEN: str = st.secrets["GITHUB_TOKEN"]  # Replace with your actual GitHub token
    MAX_FILE_SIZE: int = 1000000  # 1MB
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    MAX_TOKENS: int = 2048
    TEMPERATURE: float = 0.3
    TOP_K_RETRIEVAL: int = 5
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    GROQ_MODEL: str = "openai/gpt-oss-120b"

config = Config()
