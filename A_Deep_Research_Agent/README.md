# Agent A: Deep Research Agent for Lead Generation

Based on: [Build a Deep Research Agent with Google ADK](https://cloud.google.com/blog/products/ai-machine-learning/build-a-deep-research-agent-with-google-adk)

---

## 🧠 Overview

This agent performs deep research on companies to generate qualified leads.  
It searches the web, analyzes company information, and produces structured reports with contact details and insights.

---

## 🎥 Video Walkthrough

Watch the full step-by-step walkthrough of this project on YouTube:  
👉 [**Deep Research Agent for Lead Generation**](https://youtu.be/qKUajc8iEwc)

The video covers:
- Setting up Google ADK and environment variables  
- Running the research workflow  
- Generating reports and interpreting results  
- Customizing research depth and outputs  

---

## 🚀 Features

- 🔍 **Multi-step research workflow**  
- 🌐 **Web search integration** using Google Search  
- 📊 **Structured data extraction** for company and contact insights  
- 🧾 **CSV and JSON report generation**  
- ⚙️ **Configurable research depth and parameters**

---

## ⚙️ Setup

1. **Install dependencies**
   ```bash
   cd agent-a-deep-research
   pip install -r requirements.txt

2. **Set up environment variables**

   export GOOGLE_CLOUD_PROJECT="your-project-id"
   export GOOGLE_GENAI_USE_VERTEXAI="true"
   export GOOGLE_CLOUD_LOCATION="us-central1"

3. **Authenticate with Google Cloud**

   gcloud auth application-default login

---

## 📂 Output

The agent generates the following files in the `outputs/` directory:

| File                    | Description                                        |
| ----------------------- | -------------------------------------------------- |
| `leads_report.csv`      | Structured lead data for easy filtering and export |
| `research_summary.json` | Detailed research findings and metadata            |
| `agent_log.txt`         | Execution trace and logs for debugging             |

---

## 💡 Example Workflow

1. Enter a list of target companies or industries.
2. The agent uses Google Search and structured data APIs to gather company info.
3. It analyzes websites, extracts contacts, and ranks lead quality.
4. Results are stored in CSV and JSON formats for further processing.

---

## 🔗 Resources

* [Google ADK Documentation](https://cloud.google.com/gen-app-builder/docs/adk)
* [Vertex AI Overview](https://cloud.google.com/vertex-ai)
* [Python SDK for ADK](https://pypi.org/project/google-adk/)

---

## 🎥 Watch the Demo Again

📺 **YouTube Walkthrough:** [https://youtu.be/qKUajc8iEwc](https://youtu.be/qKUajc8iEwc)
