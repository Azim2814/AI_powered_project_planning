# 🤖 Automated Project Planning & Development using Python & AI/ML

## 📹 Demo Video
Watch the complete working demo with explanation:  
👉 [Click to Watch](https://www.loom.com/share/944989e3f8834d78ba29fd01f5723f5b?sid=5b689514-ff52-424a-a577-b2e26ff12ab3)

---

## 🧠 AI/ML Technologies Used

- **Python 3.x**: Base programming language for all automation logic.
- **spaCy**: For extracting structured data (like tasks, user stories) from natural language in the document.
- **Transformers (Hugging Face)**: To load and use pre-trained models for generating test cases.
- **FLAN-T5**: A fine-tuned open-source NLP model used to automatically write test case steps.
- **Jira REST API**: For creating issues in Jira programmatically.
- **GitHub REST API**: For automating repository creation and file structure based on Jira tickets.

---

## ⚙️ Process Followed to Automate Each Task

### 1. 📄 **Jira Ticket Creation**
- Parsed a `.docx` requirement document using Python.
- Identified user stories, tasks, and descriptions using spaCy.
- Created Jira tickets using Jira API with correct summary, description, and type.

### 2. 🗂️ **GitHub Repository Automation**
- Created a new GitHub repository using GitHub API.
- Structured folders based on ticket types (e.g., Features, Bugs, Docs).
- Added README or placeholder files in each folder automatically.

### 3. ✅ **Test Case Generation**
- Used the FLAN-T5 model to generate logical test steps based on each Jira ticket's summary and description.
- These test cases were attached to tickets and optionally added to GitHub for traceability.

---

## 🔍 Functionality & Concepts Applied

- **Natural Language Processing (NLP)**: To extract structured tasks from unstructured project descriptions.
- **Prompt Engineering**: Framing ticket descriptions as prompts to generate test cases.
- **API Integration**: Using RESTful APIs for both Jira and GitHub.
- **Automation Workflow**: Combined parsing, ticket creation, repo setup, and test generation into one seamless script.
- **AI in DevOps**: Applied AI not just for logic, but also to generate documentation (test cases), showcasing ML's role in development pipelines.

---
