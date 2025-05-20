import os
import re
import docx
import time
from pathlib import Path
from jira import JIRA
from github import Github
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from dotenv import load_dotenv

# === Load environment variables ===
load_dotenv(dotenv_path=Path(r"C:\Users\AZIM MEMON\OneDrive\Desktop\python\AI_Project_Automation\project.env"))
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
JIRA_URL = 'https://azimnathani806.atlassian.net'
JIRA_EMAIL = 'azimnathani806@gmail.com'
GITHUB_REPO = 'Azim2814/final_demo'
PROJECT_KEY = 'PDT'

# === Load AI model ===
model_name = "google/flan-t5-large"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
flan_pipeline = pipeline("text2text-generation", model=model, tokenizer=tokenizer)

# === Authenticate ===
jira = JIRA(server=JIRA_URL, basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN))
github = Github(GITHUB_TOKEN)
repo = github.get_repo(GITHUB_REPO)

# === Utilities ===
def sanitize_summary(text):
    name = re.sub(r'[^a-zA-Z0-9\\-]+', '-', text.strip().lower())

    return name.strip('-')

def extract_sections_from_docx(path):
    doc = docx.Document(path)
    sections = {}
    current_section = None
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue
        if re.match(r'^\d+\.\s+', text):  # Detect main section like "3. Venue Management"
            current_section = text
            sections[current_section] = []
        elif current_section:
            sections[current_section].append(text)
    return sections

def generate_test_case(text):
    prompt = f"Generate software test cases for the following requirement:\n{text}"
    result = flan_pipeline(prompt, max_length=256, num_return_sequences=1, do_sample=False)
    return result[0]['generated_text'].strip()

def create_jira_parent(summary, description):
    summary = sanitize_summary(summary)
    issue_dict = {
        'project': {'key': PROJECT_KEY},
        'summary': summary,
        'description': description,
        'issuetype': {'name': 'Task'}
    }
    issue = jira.create_issue(fields=issue_dict)
    print(f"✅ Parent Jira ticket created: {issue.key}")
    return issue.key

def create_jira_subtask(parent_key, summary, description, test_case):
    summary = sanitize_summary(summary)
    issue_dict = {
        'project': {'key': PROJECT_KEY},
        'summary': summary,
        'description': f"{description}\n\n### Test Cases\n{test_case}",
        'issuetype': {'name': 'Sub-task'},
        'parent': {'key': parent_key},
    }
    issue = jira.create_issue(fields=issue_dict)
    print(f"   📝 Sub-task created: {issue.key}")
    return issue.key

# def create_github_branch(branch_name, base="main"):
#     if branch_name in [b.name for b in repo.get_branches()]:
#         print(f"   ⚠️ GitHub branch already exists: {branch_name}")
#         return
#     source = repo.get_branch(base)
#     repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=source.commit.sha)
#     print(f"   ✅ GitHub branch created: {branch_name}")


def create_github_branch(branch_name, base="main"):
    branches = [b.name for b in repo.get_branches()]
    if branch_name in branches:
        print(f"   ⚠️ GitHub branch already exists: {branch_name}")
        return

    try:
        source = repo.get_branch(base)
        repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=source.commit.sha)
        print(f"   ✅ GitHub branch created: {branch_name}")
        
        # Add a short delay to ensure GitHub registers the new branch
        time.sleep(2)
    except Exception as e:
        print(f"   ❌ Failed to create branch '{branch_name}' from base '{base}': {e}")


def commit_test_case(branch_name, filename, content):
    try:
        repo.create_file(f"tests/{filename}", "Add test case", content, branch=branch_name)
        print(f"   📄 Test case committed: tests/{filename}")
    except Exception as e:
        print(f"   ❌ Error committing test case: {e}")

# === Main Pipeline ===
def main():
    doc_path = Path(r"C:\Users\AZIM MEMON\OneDrive\Desktop\python\AI_Project_Automation\requirements.docx")
    sections = extract_sections_from_docx(doc_path)

    for section_title, tasks in sections.items():
        parent_key = create_jira_parent(section_title, f"Feature: {section_title}")
        parent_branch = f"feature/{sanitize_summary(section_title)[:30]}"
        create_github_branch(parent_branch)

        for task in tasks:
            subtask_summary = task if len(task) < 100 else task[:97] + "..."
            test_case = generate_test_case(task)
            subtask_key = create_jira_subtask(parent_key, subtask_summary, task, test_case)

            sub_branch = f"{parent_branch}-{subtask_key.lower()}"
            create_github_branch(sub_branch, base=parent_branch)
            commit_test_case(sub_branch, f"{subtask_key}_test.md", test_case)

if __name__ == "__main__":
    main()
