from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter, Language
from langchain.schema import Document
from config import config

class AdvancedDocumentProcessor:
    """Advanced document processing with LangChain"""
    
    def __init__(self):
        # Initialize different splitters for different file types
        self.splitters = {
            'python': RecursiveCharacterTextSplitter.from_language(
                language=Language.PYTHON,
                chunk_size=config.CHUNK_SIZE,
                chunk_overlap=config.CHUNK_OVERLAP
            ),
            'javascript': RecursiveCharacterTextSplitter.from_language(
                language=Language.JS,
                chunk_size=config.CHUNK_SIZE,
                chunk_overlap=config.CHUNK_OVERLAP
            ),
            'java': RecursiveCharacterTextSplitter.from_language(
                language=Language.JAVA,
                chunk_size=config.CHUNK_SIZE,
                chunk_overlap=config.CHUNK_OVERLAP
            ),
            'cpp': RecursiveCharacterTextSplitter.from_language(
                language=Language.CPP,
                chunk_size=config.CHUNK_SIZE,
                chunk_overlap=config.CHUNK_OVERLAP
            ),
            'documentation': RecursiveCharacterTextSplitter.from_language(
                language=Language.MARKDOWN,
                chunk_size=config.CHUNK_SIZE,
                chunk_overlap=config.CHUNK_OVERLAP
            ),
            'default': RecursiveCharacterTextSplitter(
                chunk_size=config.CHUNK_SIZE,
                chunk_overlap=config.CHUNK_OVERLAP,
                separators=["\n\n", "\n", " ", ""]
            )
        }
    
    def process_documents(self, documents: List[Document]) -> List[Document]:
        """Process documents with appropriate splitters"""
        processed_docs = []
        
        for doc in documents:
            file_type = doc.metadata.get('file_type', 'default')
            splitter = self.splitters.get(file_type, self.splitters['default'])
            
            # Split the document
            chunks = splitter.split_documents([doc])
            
            # Add chunk information to metadata
            for i, chunk in enumerate(chunks):
                chunk.metadata.update({
                    'chunk_id': i,
                    'total_chunks': len(chunks),
                    'chunk_size': len(chunk.page_content)
                })
            
            processed_docs.extend(chunks)
        
        return processed_docs