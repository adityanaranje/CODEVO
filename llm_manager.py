import streamlit as st
from groq import Groq
from config import config

class LLMManager:
    """Manages Groq LLM"""
    
    def __init__(self):
        self.groq_client = None
        self.model = config.GROQ_MODEL
    
    def initialize_groq_llm(self, api_key: str = None):
        """Initialize Groq LLM"""
        try:
            api_key = api_key if api_key else config.GROQ_API_KEY
            self.groq_client = Groq(api_key=api_key)
            return True
        except Exception as e:
            st.error(f"Error initializing Groq: {str(e)}")
            return False
    
    def generate_response(self, prompt: str) -> str:
        """Generate response using Groq"""
        try:
            if not self.groq_client:
                return "Groq client not initialized"
                
            completion = self.groq_client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                temperature=config.TEMPERATURE,
                max_tokens=config.MAX_TOKENS
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Error generating response: {str(e)}"