# 🤖 Agent B: Advanced Tool Agent with Gemini CLI

Based on: [Combine ADK, Gemini CLI, and Cloud Run](https://medium.com/@derrickchwong/combine-adk-gemini-cli-and-cloud-run-c5dea5118853)

---

## 🧠 Overview

This project demonstrates **advanced tool integration** by combining the **Google Agent Development Kit (ADK)** with **Gemini CLI**.  
It creates a seamless pipeline where an ADK agent can invoke Gemini CLI as an external tool for **specialized code generation**, **multi-file analysis**, and **refactoring tasks**.

---

## 🎥 Video Walkthrough

📺 Watch the complete setup and demo here:  
👉 [**Advanced Tool Agent with Gemini CLI**](https://youtu.be/_fNsDxPZWdQ)

**In this video you’ll learn:**
- How the ADK agent integrates with Gemini CLI  
- Step-by-step Cloud Run deployment  
- How tool invocation and streaming responses work  
- Live demo of code generation and refactoring tasks  

---

## ⚙️ Features

- 🧩 **ADK + Gemini CLI Integration**  
- 🪄 **Tool-based architecture** for modular AI pipelines  
- 💻 **Code generation and refactoring pipeline**  
- ☁️ **Cloud Run deployment ready**  
- ⚡ **Streaming LLM responses**

---

## 🛠️ Setup

### 1️⃣ Install Dependencies
```bash
cd agent-b-gemini-cli
pip install -r requirements.txt
````

### 2️⃣ Install Gemini CLI

```bash
pip install google-generativeai
```

### 3️⃣ Set Up Environment

```bash
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_API_KEY="your-api-key"     # for Gemini CLI
export GOOGLE_GENAI_USE_VERTEXAI="true"
```

### 4️⃣ Authenticate with Google Cloud (optional for Vertex AI)

```bash
gcloud auth application-default login
```

---

## ▶️ Usage

Run the tool agent:

```bash
python tool_agent.py
```

Interactive mode:

```bash
python tool_agent.py --interactive
```

During execution, the agent will automatically:

1. Interpret the user request.
2. Choose whether Gemini CLI is required.
3. Generate code or analyze results through the CLI tool.
4. Stream the final response back to the user.

---

## 🧩 Architecture

```
User Request
      ↓
ADK Agent (Reasoning + Planning)
      ↓
Tool Invocation → Gemini CLI (Execution Engine)
      ↓
Streaming Response to User
```

The agent decides when to invoke Gemini CLI for specialized tasks such as:

* 🧠 Complex code generation
* 🗂️ Multi-file refactoring
* 🧮 Advanced static analysis
* 🧰 Tool-assisted debugging workflows

---

## 📂 Output

| File / Folder           | Description                                   |
| ----------------------- | --------------------------------------------- |
| `generated_code/`       | Code files created via Gemini CLI integration |
| `logs/`                 | Agent and tool execution logs                 |
| `tool_invocations.json` | JSON trace of Gemini CLI calls                |

---

## ☁️ Cloud Run Deployment (Optional)

You can containerize and deploy the agent to **Google Cloud Run**:

```bash
gcloud builds submit --tag gcr.io/$GOOGLE_CLOUD_PROJECT/agent-b
gcloud run deploy agent-b \
  --image gcr.io/$GOOGLE_CLOUD_PROJECT/agent-b \
  --platform managed \
  --allow-unauthenticated \
  --region us-central1
```

Then access it via:

```
https://agent-b-<PROJECT_NUMBER>.us-central1.run.app
```

---

## 🔍 Example Commands

**Code Generation**

```text
"Generate a Python function to scrape product data from an e-commerce site."
```

**Refactoring**

```text
"Refactor the data cleaning module for parallel processing and improve readability."
```

**Analysis**

```text
"Explain how the Gemini tool decides between async and sync execution modes."
```

---

## 🧠 How It Works

1. **ADK Agent** parses user intent.
2. If the request requires code generation or analysis, the agent selects the Gemini CLI tool.
3. Gemini CLI executes the task and returns structured output.
4. ADK formats and streams the final result to the user.

---

## 🔗 Resources

* [Google ADK Documentation](https://cloud.google.com/gen-app-builder/docs/adk)
* [Gemini CLI Documentation](https://pypi.org/project/google-generativeai)
* [Vertex AI Gemini Models](https://cloud.google.com/vertex-ai/docs/generative-ai)
* [Cloud Run Docs](https://cloud.google.com/run/docs)

---

## 🎥 Watch the Demo Again

📺 **YouTube:** [https://youtu.be/_fNsDxPZWdQ](https://youtu.be/_fNsDxPZWdQ)
