def load_uploaded_files(uploaded_files):
    repo_text = ""
    for file in uploaded_files:
        try:
            content = file.read().decode("utf-8")
            repo_text += f"\n\n📂 FILE: {file.name}\n{'-'*50}\n{content}\n"
        except Exception:
            continue
    return repo_text
