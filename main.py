import streamlit as st
import re
from github_repository import GitHubRepository
from rag_system import AdvancedRAGSystem
from code_generate import CodeGenerate


def main():
    st.set_page_config(
        page_title="Codevo",
        page_icon="pageicon.svg",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Sidebar configuration
    st.sidebar.image("sidebar.png")

    st.sidebar.markdown("---")

    task = st.sidebar.radio("🔧 Choose Task", ["Repo Q&A", "Generate Code"])
    
    # Repository Input
    if task == "Repo Q&A":
        st.header("GitHub Repository Q&A Bot")
        st.sidebar.header("📁 Repository")
        repo_url = st.sidebar.text_input(
            "GitHub Repository URL",
            placeholder="https://github.com/langchain-ai/langchain"
        )
        
        # Parse repository URL
        repo_owner = ""
        repo_name = ""
        if repo_url:
            match = re.match(r'https://github\.com/([^/]+)/([^/]+)', repo_url.strip())
            if match:
                repo_owner = match.group(1)
                repo_name = match.group(2)
            else:
                st.sidebar.error("Please enter a valid GitHub repository URL")
        
        # Process Repository Button
        process_button = st.sidebar.button(
            "🔄 Process Repository", 
            type="primary",
            help="This may take a few minutes for large repositories"
        )
    else:
        st.header("Generate Code")
    
    
    # Initialize session state
    if 'rag_system' not in st.session_state:
        st.session_state.rag_system = None
    if 'repository_processed' not in st.session_state:
        st.session_state.repository_processed = False
    if 'current_repo' not in st.session_state:
        st.session_state.current_repo = ""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # For repository Q&A
    if task=="Repo Q&A":
        # Process repository
        if process_button and repo_owner and repo_name:
            current_repo = f"{repo_owner}/{repo_name}"
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Initialize RAG system
                status_text.text("Initializing RAG system...")
                progress_bar.progress(10)
                
                rag_system = AdvancedRAGSystem()
                
                # Setup LLM
                status_text.text("Setting up Groq language model...")
                progress_bar.progress(20)
                
                llm_success = rag_system.setup_llm()
                
                if not llm_success:
                    st.error("Failed to initialize Groq language model. Please check your API key in config.py")
                    return
                
                # Crawl repository
                status_text.text(f"Crawling repository {current_repo}...")
                progress_bar.progress(40)
                
                github_client = GitHubRepository()
                documents = github_client.crawl_repository(repo_owner, repo_name)
                
                if not documents:
                    st.error("No processable files found in repository")
                    return
                
                st.info(f"Found {len(documents)} files")
                
                # Process repository
                status_text.text("Processing documents and creating embeddings...")
                progress_bar.progress(70)
                
                success = rag_system.process_repository(documents)
                
                if not success:
                    st.error("Failed to process repository")
                    return
                
                progress_bar.progress(100)
                status_text.text("Repository processed successfully!")
                
                # Store in session state
                st.session_state.rag_system = rag_system
                st.session_state.repository_processed = True
                st.session_state.current_repo = current_repo
                st.session_state.chat_history = []
                
                st.balloons()
                st.success(f"🎉 Repository **{current_repo}** processed successfully!")
                
            except Exception as e:
                st.error(f"Error processing repository: {str(e)}")
                progress_bar.empty()
                status_text.empty()
        
        # Query Interface
        if st.session_state.repository_processed and st.session_state.rag_system:
            st.header("💬 Chat with Repository")
            
            # Query input
            question = st.text_input(
                "Ask a question about the repository:",
                placeholder="How does the authentication work? What are the main components?",
                key="question_input"
            )
            
            if st.button("🔍 Ask Question") and question:
                with st.spinner("Generating answer..."):
                    result = st.session_state.rag_system.query(question)
                    
                    # Add to chat history
                    st.session_state.chat_history.append({"question": question, "answer": result})
                    
                    # Display answer
                    st.subheader("💡 Answer")
                    st.write(result['answer'])
                    
                    # Display sources
                    if result['sources']:
                        st.subheader("📚 Sources")
                        for i, source in enumerate(result['sources']):
                            metadata = source.metadata
                            source_title = f"📄 {metadata.get('source', 'Unknown')} ({metadata.get('file_type', 'text')})"
                            
                            with st.expander(source_title):
                                # Show metadata
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.markdown(f"**File:** `{metadata.get('file_name', 'N/A')}`")
                                    st.markdown(f"**Type:** {metadata.get('file_type', 'N/A')}")
                                with col2:
                                    st.markdown(f"**Chunk:** {metadata.get('chunk_id', 0) + 1}/{metadata.get('total_chunks', 1)}")
                                    st.markdown(f"**Size:** {metadata.get('chunk_size', len(source.page_content))} chars")
                                
                                # Show content
                                st.markdown("**Content:**")
                                content = source.page_content[:1000] + "..." if len(source.page_content) > 1000 else source.page_content
                                st.code(content, language=metadata.get('file_type', 'text'))
                                
                                # Link to GitHub
                                if 'url' in metadata:
                                    st.markdown(f"[View on GitHub]({metadata['url']})")
            
            # Chat History
            if st.session_state.chat_history:
                st.header("📝 Chat History")
                for i, chat in enumerate(reversed(st.session_state.chat_history[-5:])):  # Show last 5
                    with st.expander(f"Q{len(st.session_state.chat_history) - i}: {chat['question'][:50]}..."):
                        st.markdown(f"**Question:** {chat['question']}")
                        st.markdown(f"**Answer:** {chat['answer']['answer']}")
        
        # Repository Analysis
        if st.session_state.repository_processed:
            st.header("📊 Repository Analysis")
            
            if st.button("🔍 Analyze Repository Structure"):
                with st.spinner("Analyzing repository..."):
                    analysis_questions = [
                        "What programming languages are primarily used in this repository?",
                        "What is the overall project structure and organization?",
                        "What are the main entry points or important files?"
                    ]
                    
                    analysis_results = []
                    for q in analysis_questions:
                        result = st.session_state.rag_system.query(q)
                        analysis_results.append({"question": q, "answer": result['answer']})
                    
                    for analysis in analysis_results:
                        st.subheader(analysis['question'])
                        st.write(analysis['answer'])
                        st.markdown("---")
    else:
        query = st.chat_input("Enter you problem statement....")

        if query:
            generate = CodeGenerate()
            response = generate.generate_code(query)
            st.markdown(response)

    # Footer with additional features
    st.markdown("---")

    # Technical Information
    if task=="Repo Q&A":
        with st.expander("🔧 Technical Details"):
            st.markdown("""
            ### Libraries Used:
            - **LangChain**: Document processing, text splitting, and embeddings
            - **HuggingFace**: Embeddings model
            - **Groq**: Fast cloud-based LLM inference
            - **FAISS**: Vector storage and similarity search
            - **Streamlit**: Interactive web interface
            
            ### Key Components:
            1. **GitHubRepository**: Handles GitHub API interactions and file crawling
            2. **AdvancedDocumentProcessor**: Language-aware document chunking
            3. **EmbeddingManager**: FAISS vector store creation and similarity search
            4. **LLMManager**: Groq LLM provider support
            5. **AdvancedRAGSystem**: Orchestrates the entire RAG pipeline
            
            ### Performance Tips:
            - Groq provides fast responses with high quality
            - FAISS ensures efficient similarity search
            - Language-aware chunking preserves code context
            - GitHub tokens improve API rate limits
            """)
    

    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center'>
        <p>Built with ❤️ using <strong>LangChain</strong>, <strong>HuggingFace</strong>, <strong>Groq</strong>, and <strong>Streamlit</strong></p>
        <p>🌟 Advanced RAG System for GitHub Repository Analysis and Code Generation</p>
                <p>--- By <strong>Aditya Naranje</strong> ---</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()