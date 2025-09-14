import requests
import streamlit as st

def fetch_github_repo(owner, repo, branch, extensions, GITHUB_TOKEN):
    api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {GITHUB_TOKEN}" if GITHUB_TOKEN else None
    }
    response = requests.get(api_url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch repo: {response.text}")
    tree = response.json().get("tree", [])

    repo_text = ""
    for item in tree:
        if item["type"] == "blob":
            path = item["path"]
            if not any(path.endswith(ext) for ext in extensions):
                continue
            file_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"
            file_resp = requests.get(file_url)
            if file_resp.status_code == 200:
                try:
                    repo_text += f"\n\n📂 PATH: {path}\n{'-'*50}\n{file_resp.text}\n"
                except Exception:
                    continue
    return repo_text

def get_github_branches(owner, repo, GITHUB_TOKEN):
    url = f"https://api.github.com/repos/{owner}/{repo}/branches"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {GITHUB_TOKEN}" if GITHUB_TOKEN else None
    }
    r = requests.get(url, headers=headers)
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()  # Raise HTTPError if status_code != 200
        return [branch["name"] for branch in r.json()]
    except requests.exceptions.RequestException as e:
        # Raise original exception with detailed info
        raise Exception(f"Failed to fetch branches: {e}") from e
        #st.error("The link provided is invalid!!!")




