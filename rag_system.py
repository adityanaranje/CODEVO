from typing import List, Dict, Any
from langchain.schema import Document
from langchain.prompts import PromptTemplate
from embedding_manager import EmbeddingManager
from llm_manager import LLMManager
from document_processor import AdvancedDocumentProcessor
from config import config

class AdvancedRAGSystem:
    """Advanced RAG system using Groq and FAISS"""
    
    def __init__(self):
        self.embedding_manager = EmbeddingManager()
        self.llm_manager = LLMManager()
        self.document_processor = AdvancedDocumentProcessor()
        
        # Custom prompt template
        self.prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template="""You are an expert software engineer and documentation analyst. Based on the provided context from a GitHub repository, answer the user's question comprehensively and accurately.

            Context from repository files:
            {context}

            Question: {question}

            Instructions:
            - Provide a detailed, technical answer based on the repository context
            - Reference specific files, functions, or code sections when relevant
            - If you need to show code examples, use proper formatting
            - If the context doesn't contain sufficient information, clearly state what's missing
            - Be helpful and educational in your explanations
            - Include practical advice when applicable

            Answer:"""
        )
    
    def setup_llm(self, api_key: str = None) -> bool:
        """Setup Groq LLM"""
        return self.llm_manager.initialize_groq_llm(api_key)
    
    def process_repository(self, documents: List[Document]) -> bool:
        """Process repository documents and create vector store"""
        # Process documents
        processed_docs = self.document_processor.process_documents(documents)
        
        if not processed_docs:
            return False
        
        # Create FAISS vector store
        success = self.embedding_manager.create_vector_store(processed_docs)
        
        return success
    
    def query(self, question: str) -> Dict[str, Any]:
        """Query the RAG system"""
        try:
            return self._query_with_groq(question)
        except Exception as e:
            return {"answer": f"Error processing query: {str(e)}", "sources": []}
    
    def _query_with_groq(self, question: str) -> Dict[str, Any]:
        """Query using Groq with manual RAG pipeline"""
        # Get relevant documents
        relevant_docs = self.embedding_manager.similarity_search(question)
        
        if not relevant_docs:
            return {
                "answer": "I couldn't find any relevant information in the repository to answer your question.",
                "sources": []
            }
        
        # Build context
        context = "\n\n".join([
            f"File: {doc.metadata.get('source', 'Unknown')}\n{doc.page_content}"
            for doc in relevant_docs
        ])
        
        # Generate prompt
        prompt = self.prompt_template.format(context=context, question=question)
        
        # Get response
        answer = self.llm_manager.generate_response(prompt)
        
        return {
            "answer": answer,
            "sources": relevant_docs
        }
    
    def get_repository_stats(self) -> Dict[str, Any]:
        """Get statistics about the processed repository"""
        if not self.embedding_manager.vector_store:
            return {}
        
        return {
            "embedding_model": self.embedding_manager.model_name,
            "llm_model": self.llm_manager.model,
            "vector_store": "FAISS"
        }