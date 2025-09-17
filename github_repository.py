import os
import requests
import base64
from typing import List, Dict, Optional
import streamlit as st
from langchain.text_splitter import Language
from langchain.schema import Document
from config import config

class GitHubRepository:
    """Enhanced GitHub repository handler with better file processing"""
    
    def __init__(self, token: str = None):
        self.token = token if token else config.GITHUB_TOKEN
        self.headers = {'Authorization': f'token {self.token}'} if self.token else {}
        self.supported_extensions = {
            '.py': Language.PYTHON,
            '.js': Language.JS,
            '.ts': Language.JS,
            '.jsx': Language.JS,
            '.tsx': Language.JS,
            '.java': Language.JAVA,
            '.cpp': Language.CPP,
            '.c': Language.CPP,
            '.cs': Language.CSHARP,
            '.php': Language.PHP,
            '.rb': Language.RUBY,
            '.go': Language.GO,
            '.rs': Language.RUST,
            '.scala': Language.SCALA,
            '.kt': Language.KOTLIN,
            '.md': Language.MARKDOWN,
            '.html': Language.HTML,
            '.sol': Language.SOL
        }
    
    def get_repo_info(self, owner: str, repo: str) -> Dict:
        """Get repository metadata"""
        url = f"https://api.github.com/repos/{owner}/{repo}"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        return {}
    
    def get_repo_structure(self, owner: str, repo: str, path: str = "") -> List[Dict]:
        """Get repository structure with enhanced metadata"""
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code != 200:
            st.error(f"Error fetching repository: {response.status_code}")
            return []
        
        return response.json()
    
    def get_file_content(self, file_data: Dict) -> Optional[str]:
        """Enhanced file content retrieval with better error handling"""
        try:
            if file_data.get('size', 0) > config.MAX_FILE_SIZE:
                return None
            
            response = requests.get(file_data['url'], headers=self.headers)
            if response.status_code != 200:
                return None
            
            file_info = response.json()
            content = base64.b64decode(file_info['content']).decode('utf-8')
            return content
            
        except Exception as e:
            st.warning(f"Could not read {file_data.get('path', 'unknown file')}: {str(e)}")
            return None
    
    def crawl_repository(self, owner: str, repo: str, max_depth: int = 3) -> List[Document]:
        """Enhanced repository crawler that returns LangChain Documents"""
        documents = []
        
        def _crawl_recursive(path: str = "", current_depth: int = 0):
            if current_depth > max_depth:
                return
            
            items = self.get_repo_structure(owner, repo, path)
            
            for item in items:
                if item['type'] == 'file' and self._is_processable_file(item['name']):
                    content = self.get_file_content(item)
                    if content:
                        # Create LangChain Document with metadata
                        doc = Document(
                            page_content=content,
                            metadata={
                                'source': item['path'],
                                'file_name': item['name'],
                                'file_type': self._get_file_type(item['name']),
                                'url': item['html_url'],
                                'size': item.get('size', 0),
                                'repository': f"{owner}/{repo}"
                            }
                        )
                        documents.append(doc)
                        
                elif item['type'] == 'dir' and not self._should_skip_directory(item['name']):
                    _crawl_recursive(item['path'], current_depth + 1)
        
        _crawl_recursive()
        return documents
    
    def _is_processable_file(self, filename: str) -> bool:
        """Enhanced file filtering"""
        # Programming files
        code_extensions = {'.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', 
                          '.cs', '.php', '.rb', '.go', '.rs', '.scala', '.kt', '.sol', '.r'}
        
        # Documentation files
        doc_extensions = {'.md', '.rst', '.txt', '.adoc'}
        
        # Configuration files
        config_extensions = {'.json', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf'}
        
        # Web files
        web_extensions = {'.html', '.css', '.scss', '.less'}
        
        # Special files
        special_files = {'README', 'LICENSE', 'CHANGELOG', 'CONTRIBUTING', 'DOCKERFILE', 'MAKEFILE'}
        
        file_ext = os.path.splitext(filename)[1].lower()
        file_name = os.path.splitext(filename)[0].upper()
        
        return (file_ext in code_extensions or 
                file_ext in doc_extensions or 
                file_ext in config_extensions or 
                file_ext in web_extensions or 
                file_name in special_files)
    
    def _get_file_type(self, filename: str) -> str:
        """Get file type for better processing"""
        ext = os.path.splitext(filename)[1].lower()
        
        if ext in {'.py'}: return 'python'
        elif ext in {'.js', '.ts', '.jsx', '.tsx'}: return 'javascript'
        elif ext in {'.java'}: return 'java'
        elif ext in {'.cpp', '.c'}: return 'cpp'
        elif ext in {'.md', '.rst'}: return 'documentation'
        elif ext in {'.json', '.yaml', '.yml'}: return 'configuration'
        elif ext in {'.html', '.css'}: return 'web'
        else: return 'text'
    
    def _should_skip_directory(self, dirname: str) -> bool:
        """Skip common directories that don't contain useful code"""
        skip_dirs = {
            'node_modules', '.git', '__pycache__', '.pytest_cache',
            'venv', '.venv', 'env', '.env', 'dist', 'build',
            '.next', '.nuxt', 'coverage', '.coverage', 'logs',
            '.DS_Store', '.idea', '.vscode'
        }
        return dirname.lower() in skip_dirs