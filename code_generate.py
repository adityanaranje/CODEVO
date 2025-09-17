from langchain_groq import ChatGroq
from config import config
from langchain.prompts import PromptTemplate

class CodeGenerate:

    def __init__(self):
        self.llm = ChatGroq(
            groq_api_key = config.GROQ_API_KEY,
            model = "llama-3.3-70b-versatile",
            temperature=0
        )

    def generate_code(self, query):
        chat_prompt = PromptTemplate.from_template(
            """
            You are an expert software engineer. 
            Generate the **best possible code** for the following task:

            Task: {query}

            Guidelines:
            - Write clean, efficient, and bug-free code.
            - Use best coding practices (readability, modularity).
            - Add concise comments where needed.
            - Prefer clarity over cleverness.
            - If multiple approaches exist, choose the most efficient and maintainable.

            Return only the complete code block.
            """
        )

        chain = chat_prompt | self.llm
        resp = chain.invoke({"query": query})
        return resp.content