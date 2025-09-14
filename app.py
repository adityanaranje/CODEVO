import os
import streamlit as st
from utils.github_loader import fetch_github_repo, get_github_branches
from utils.file_loader import load_uploaded_files
from utils.qa_chain import build_qa_chain
from utils.code_gen import generate_code
import requests

# --- Streamlit App ---
st.set_page_config(page_title="Codevo", layout="wide", page_icon="pageicon.svg")
st.sidebar.image("sidebar.png")

# --- GitHub Token Input ---
st.sidebar.title("🔑 GitHub Access Token")
github_token = st.sidebar.text_input(
    "Enter your GitHub Personal Access Token (required for large repos)",
    type="password"
)

# Store token in session_state for reuse
if github_token:
    st.session_state["GITHUB_TOKEN"] = github_token
else:
    st.warning("GitHub token required to fetch branches and repo.")
    st.stop()  # Stop further execution until token is provided

# --- Function to validate token ---
def validate_github_token(token):
    url = "https://api.github.com/user"
    headers = {"Authorization": f"token {token}"}
    r = requests.get(url, headers=headers)
    return r.status_code == 200

if not validate_github_token(st.session_state["GITHUB_TOKEN"]):
    st.error("Invalid GitHub token! Please provide a correct token.")
    st.stop()  # Stop further execution

# --- Sidebar task selection ---
st.sidebar.title("🔍 Choose Task")
task = st.sidebar.radio("Select one:", ["Q&A Bot", "Code Generator"])

# --- Session state setup ---
if "qa_github_history" not in st.session_state:
    st.session_state["qa_github_history"] = []
if "qa_upload_history" not in st.session_state:
    st.session_state["qa_upload_history"] = []
if "code_history" not in st.session_state:
    st.session_state["code_history"] = []

if "repo_github_text" not in st.session_state:
    st.session_state["repo_github_text"] = ""
if "repo_upload_text" not in st.session_state:
    st.session_state["repo_upload_text"] = ""

if "branches" not in st.session_state:
    st.session_state["branches"] = []
if "selected_branch" not in st.session_state:
    st.session_state["selected_branch"] = "main"

if "vectorstores" not in st.session_state:
    st.session_state["vectorstores"] = {}

# Only fetch useful file types to speed up repo loading
extensions = [
    ".json", ".md", ".html", ".js", ".py", ".css",".cs",".txt",
    ".ts",".tsx",".jsx", ".java", ".go", ".c", ".cpp", ".rb", ".php", ".sh", ".ipynb"
]

# --- Task 1: Q&A Bot ---
if task == "Q&A Bot":
    option = st.sidebar.radio("Input Source:", ["GitHub Repo", "Upload Files"])

    # ---- GitHub Repo Option ----
    if option == "GitHub Repo":
        st.title("🤖 Q&A Bot for GitHub Repo")
        repo_url = st.sidebar.text_input("Enter GitHub Repo URL")

        # Use token in headers for all GitHub requests
        headers = {"Authorization": f"token {st.session_state['GITHUB_TOKEN']}"}

        if st.sidebar.button("Get Branches"):
            try:
                if repo_url:
                    parts = repo_url.strip("/").split("/")
                    owner, repo = parts[-2], parts[-1]
                    branches = get_github_branches(owner, repo,GITHUB_TOKEN = github_token)
                    if branches:
                        st.session_state["branches"] = branches
                        st.success("✅ Branches fetched successfully!")
            except Exception as e:
                st.error(f"Failed to fetch branches: {e}")

        if st.session_state["branches"]:
            st.session_state["selected_branch"] = st.sidebar.selectbox(
                "Select branch:", st.session_state["branches"]
            )

            if st.sidebar.button("Load Repo"):
                with st.spinner("Fetching repo..."):
                    try:
                        if repo_url and st.session_state["selected_branch"]:
                            parts = repo_url.strip("/").split("/")
                            owner, repo = parts[-2], parts[-1]
                            repo_text = fetch_github_repo(
                                owner, repo, st.session_state["selected_branch"], extensions, GITHUB_TOKEN = github_token
                            )
                            st.session_state["repo_github_text"] = repo_text
                            st.sidebar.success("Repo loaded successfully!", icon="✅")
                    except Exception as e:
                        st.error(f"Invalid repo or branch: {e}")

        if st.session_state["repo_github_text"]:
            repo_name = repo_url.strip("/").split("/")[-1]
            if repo_name not in st.session_state["vectorstores"]:
                qa_chain = build_qa_chain(st.session_state["repo_github_text"], repo_name)
                st.session_state["vectorstores"][repo_name] = qa_chain
            else:
                qa_chain = st.session_state["vectorstores"][repo_name]

            chat_container = st.container()
            with chat_container:
                for chat in st.session_state["qa_github_history"]:
                    with st.chat_message("user"):
                        st.markdown(chat["user"])
                    with st.chat_message("assistant"):
                        st.code(chat["bot"], language="python")

            query = st.chat_input("Ask a question about the GitHub repo...")
            if query:
                st.session_state["qa_github_history"].append({"user": query, "bot": "..."})
                with st.spinner("🤖 Thinking..."):
                    context_window = 3
                    context = ""
                    for chat in st.session_state["qa_github_history"][-context_window:-1]:
                        context += f"Q: {chat['user']}\nA: {chat['bot']}\n"
                    full_query = context + f"Q: {query}\nA:"

                    result = qa_chain.invoke({"query": full_query})
                    answer = result["result"]

                st.session_state["qa_github_history"][-1]["bot"] = answer
                st.rerun()

    # ---- Upload Files Option ----
    elif option == "Upload Files":
        st.title("🤖 Q&A Bot for uploaded files")
        uploaded_files = st.sidebar.file_uploader(
            "Upload multiple code files",
            type=[ext[1:] for ext in extensions],
            accept_multiple_files=True
        )
        if uploaded_files:
            st.session_state["repo_upload_text"] = load_uploaded_files(uploaded_files)
            st.sidebar.success("✅ Files loaded successfully!")

        if st.session_state["repo_upload_text"]:
            qa_chain = build_qa_chain(st.session_state["repo_upload_text"], "uploaded_files")

            chat_container = st.container()
            with chat_container:
                for chat in st.session_state["qa_upload_history"]:
                    with st.chat_message("user"):
                        st.markdown(chat["user"])
                    with st.chat_message("assistant"):
                        st.code(chat["bot"], language="python")

            query = st.chat_input("Ask a question about uploaded files...")
            if query:
                st.session_state["qa_upload_history"].append({"user": query, "bot": "..."})
                with st.spinner("🤖 Thinking..."):
                    context_window = 3
                    context = ""
                    for chat in st.session_state["qa_upload_history"][-context_window:-1]:
                        context += f"Q: {chat['user']}\nA: {chat['bot']}\n"
                    full_query = context + f"Q: {query}\nA:"

                    result = qa_chain.invoke({"query": full_query})
                    answer = result["result"]

                st.session_state["qa_upload_history"][-1]["bot"] = answer
                st.rerun()

# --- Task 2: Code Generator ---
elif task == "Code Generator":
    st.title("🛠️ AI Code Generator")

    chat_container = st.container()
    with chat_container:
        for chat in st.session_state["code_history"]:
            with st.chat_message("user"):
                st.markdown(chat["user"])
            with st.chat_message("assistant"):
                st.code(chat["bot"], language="python")

    user_prompt = st.chat_input("Enter your prompt for code generation...")
    if user_prompt:
        st.session_state["code_history"].append({"user": user_prompt, "bot": "..."})
        with st.spinner("⚡ Generating code..."):
            context = ""
            for chat in st.session_state["code_history"][:-1]:
                context += f"User Prompt: {chat['user']}\nGenerated Code:\n{chat['bot']}\n\n"
            full_prompt = context + f"User Prompt: {user_prompt}\nPlease generate the code accordingly."

            response = generate_code(full_prompt)
        
        st.session_state["code_history"][-1]["bot"] = response
        st.rerun()

