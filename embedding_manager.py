import streamlit as st
from typing import List
from langchain.schema import Document
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from config import config

class EmbeddingManager:
    """Manages embeddings and FAISS vector store"""
    
    def __init__(self, model_name: str = config.EMBEDDING_MODEL):
        self.model_name = model_name
        self.embeddings = None
        self.vector_store = None
    
    def initialize_embeddings(self):
        """Initialize HuggingFace embeddings"""
        try:
            self.embeddings = HuggingFaceEmbeddings(
                model_name=self.model_name,
                model_kwargs={'device': 'cpu'},  # Use GPU if available
                encode_kwargs={'normalize_embeddings': True}
            )
            return True
        except Exception as e:
            st.error(f"Error initializing embeddings: {str(e)}")
            return False
    
    def create_vector_store(self, documents: List[Document]) -> bool:
        """Create FAISS vector store from documents"""
        if not self.embeddings:
            if not self.initialize_embeddings():
                return False
        
        try:
            self.vector_store = FAISS.from_documents(documents, self.embeddings)
            return True
        except Exception as e:
            st.error(f"Error creating vector store: {str(e)}")
            return False
    
    def similarity_search(self, query: str, k: int = config.TOP_K_RETRIEVAL) -> List[Document]:
        """Search for similar documents"""
        if not self.vector_store:
            return []
        
        return self.vector_store.similarity_search(query, k=k)