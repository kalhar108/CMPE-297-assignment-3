#  Agent C: MCP Tools-based Bug Assistant

Based on: [Tools Make an Agent from Zero to Assistant with ADK](https://cloud.google.com/blog/topics/developers-practitioners/tools-make-an-agent-from-zero-to-assistant-with-adk)

---

##  Overview

This agent leverages **Model Context Protocol (MCP) tools** to provide intelligent, automated **bug analysis and fixing**.  
It can scan source code, identify potential issues, suggest fixes, and even generate and apply patches — all within a configurable developer workflow.

---

##  Video Walkthrough

 Watch the full step-by-step walkthrough of this project on YouTube:  
 [**MCP Bug Assistant**](https://youtu.be/H8w-ZQg-qlk)

**What you'll learn in the video:**
- How MCP tools power contextual debugging  
- Setting up and running the agent  
- Performing automated bug analysis and patching  
- Integrating the assistant into a CI/CD workflow  

---

## ⚙️ Features

- 🔍 **Code analysis** powered by MCP tools  
- 🧩 **Bug detection and classification** with severity levels  
- 🪄 **Automated fix suggestions** with explanations  
- 🧵 **Patch generation & application** for one-click fixes  
- 🔄 **Integration with version control systems** (Git-ready)

---

## 🛠️ Setup

### 1️⃣ Install Dependencies
```bash
cd agent-c-mcp-bug-assistant
pip install -r requirements.txt
````

### 2️⃣ Configure Environment

```bash
cp .env.example .env
# Edit .env with your project details (e.g., API keys, repo paths)
```

### 3️⃣ (Optional) Authenticate with Google Cloud

If your MCP setup uses ADK or AlloyDB:

```bash
gcloud auth application-default login
```

---

## ▶️ Usage

### Analyze a File for Bugs

```bash
python bug_assistant.py --file path/to/code.py
```

### Start an Interactive Debugging Session

```bash
python bug_assistant.py --interactive
```

### Analyze an Entire Directory

```bash
python bug_assistant.py --directory ./src
```

---

## 🧩 MCP Tools Used

| Tool Name      | Description                                                  |
| -------------- | ------------------------------------------------------------ |
| `analyze_code` | Performs static code analysis and identifies logical issues  |
| `detect_bugs`  | Detects potential bugs and assigns severity levels           |
| `suggest_fix`  | Generates fix recommendations using contextual reasoning     |
| `apply_patch`  | Creates and applies `.patch` files directly to your codebase |

---

## 📂 Output

| File / Folder          | Description                                             |
| ---------------------- | ------------------------------------------------------- |
| `reports/`             | Detailed bug reports and summaries                      |
| `patches/`             | Generated patch files (`.patch`) for direct application |
| `logs/`                | Execution traces and debugging logs                     |
| `fix_suggestions.json` | AI-generated fix recommendations with explanations      |

Example output snippet:

```
[Bug Detected] Variable 'userData' may be undefined in main.py:42
[Severity] High
[Suggested Fix] Initialize 'userData' before first use.
[Patch] patches/main_fix_001.patch
```

---

## 🧱 Architecture

```
Source Code
    ↓
MCP Tools Layer (Analyze → Detect → Suggest → Patch)
    ↓
ADK Agent (Reasoning & Orchestration)
    ↓
Developer / CI System
```

**Flow Explanation:**

1. The agent analyzes the code using MCP’s static and dynamic analysis tools.
2. It detects bug patterns and suggests fixes with reasoning.
3. Optionally, it can auto-generate `.patch` files and apply them.
4. The workflow can integrate with version control (e.g., GitHub Actions).

---

## ☁️ Optional: Cloud Run Deployment

Containerize and deploy the assistant to Google Cloud Run:

```bash
gcloud builds submit --tag gcr.io/$GOOGLE_CLOUD_PROJECT/agent-c
gcloud run deploy agent-c \
  --image gcr.io/$GOOGLE_CLOUD_PROJECT/agent-c \
  --platform managed \
  --allow-unauthenticated \
  --region us-central1
```

Then visit:

```
https://agent-c-<PROJECT_NUMBER>.us-central1.run.app
```

---

## 🔗 Resources

* [Google ADK Documentation](https://cloud.google.com/gen-app-builder/docs/adk)
* [Model Context Protocol (MCP)](https://cloud.google.com/gen-app-builder/docs/mcp)
* [Vertex AI Gemini](https://cloud.google.com/vertex-ai)
* [Cloud Run Documentation](https://cloud.google.com/run/docs)
