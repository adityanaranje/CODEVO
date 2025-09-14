from langchain_groq import ChatGroq
import os
def generate_code(prompt):
    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="meta-llama/llama-4-maverick-17b-128e-instruct",
        temperature=0.2
    )
    response = llm.predict(prompt)
    return response
