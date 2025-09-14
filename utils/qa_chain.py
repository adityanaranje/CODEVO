import os
import pickle
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()

CACHE_DIR = "./cache"
os.makedirs(CACHE_DIR, exist_ok=True)

def build_qa_chain(repo_text, repo_name):
    """
    Build or load cached QA chain for a GitHub repo.
    """
    cache_file = os.path.join(CACHE_DIR, f"{repo_name}_faiss.pkl")

    # Load vectorstore from cache if exists
    if os.path.exists(cache_file):
        vectorstore = pickle.load(open(cache_file, "rb"))
    else:
        # Split repo text into smaller chunks for faster retrieval
        splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
        docs = splitter.create_documents([repo_text])

        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            cache_folder="./hf_models"
        )

        vectorstore = FAISS.from_documents(docs, embeddings)
        pickle.dump(vectorstore, open(cache_file, "wb"))

    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    # Use ChatGroq LLM (consider smaller model for faster responses)
    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="meta-llama/llama-4-maverick-17b-128e-instruct",  # smaller & faster
        temperature=0
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    return qa_chain

