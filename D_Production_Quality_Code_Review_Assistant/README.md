# 🚀 Building a Production AI Code Review Assistant with Google ADK

### 🎥 **YouTube Walkthrough**

👉 [Watch the full video walkthrough here](https://youtu.be/7ZWBCcM8r2g)

---

## 🧠 Overview

This project is based on Google’s official codelab **“Building a Production AI Code Review Assistant with Google ADK”** by *Ayo Adedeji*.
It walks through the process of creating a **production-grade AI Code Review Assistant** that can analyze, test, and fix Python code automatically using **Google’s Agent Development Kit (ADK)** and **Vertex AI**.

### 🔍 What It Does

* Analyzes code structure using Python’s AST
* Checks for PEP8 style compliance
* Generates and executes real test cases
* Synthesizes feedback with suggestions
* Automatically fixes broken code through a retry loop
* Deploys to Google Cloud (Vertex AI Agent Engine)
* Provides full observability with Cloud Trace

---

## 🏗️ Architecture Overview

This system is built on a **multi-agent architecture** using Google ADK:

| Agent                       | Role            | Description                                      |
| --------------------------- | --------------- | ------------------------------------------------ |
| 🧩 **Code Analyzer**        | Tool-based      | Parses AST to understand code structure          |
| 🎨 **Style Checker**        | Tool-based      | Validates PEP8 compliance and naming conventions |
| 🧪 **Test Runner**          | Execution-based | Runs real test cases in a secure sandbox         |
| 💬 **Feedback Synthesizer** | Reasoning-based | Combines all analysis into actionable feedback   |
| 🔁 **Fix Loop**             | Loop Agent      | Generates fixes and revalidates until success    |
| 🔧 **Fix Synthesizer**      | Summary Agent   | Produces the final corrected code and metrics    |

---

## ⚙️ Setup Instructions

### 1️⃣ Prerequisites

* Google Cloud Project with billing enabled
* Cloud Shell or local environment with `gcloud` installed
* Python 3.10+
* Vertex AI API enabled

### 2️⃣ Clone the Project

```bash
git clone https://github.com/ayoisio/adk-code-review-assistant.git
cd adk-code-review-assistant
git checkout codelab
```

### 3️⃣ Create a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 4️⃣ Install Dependencies

```bash
pip install -r code_review_assistant/requirements.txt
pip install -e .
```

### 5️⃣ Configure Environment

Copy the example `.env` file:

```bash
cp .env.example .env
```

Update the following in `.env`:

```bash
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_GENAI_USE_VERTEXAI=TRUE
```

### 6️⃣ Enable Required APIs

```bash
gcloud services enable \
    aiplatform.googleapis.com \
    compute.googleapis.com \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    artifactregistry.googleapis.com \
    storage.googleapis.com \
    cloudtrace.googleapis.com
```

---

## 🧪 Testing Locally

To start the development server:

```bash
adk web code_review_assistant
```

Once running, open the **ADK Dev UI** (port 8000) and select:

```
Agent: code_review_assistant
```

Then paste this code for analysis:

```python
def dfs_search_v1(graph, start, target):
    """Find if target is reachable from start."""
    visited = set()
    stack = start

    while stack:
        current = stack.pop()

        if current == target:
            return True

        if current not in visited:
            visited.add(current)
            for neighbor in graph[current]:
                if neighbor not in visited:
                    stack.append(neighbor)
    return False
```

---

## 🧩 Example Output

### **Stage 1 — Review Pipeline**

✅ **Analyzes structure:** Detects 1 function
✅ **Checks style:** Score 88/100
✅ **Runs tests:** Detects `AttributeError` bug
✅ **Synthesizes feedback:**

> “Critical bug detected at line 5: stack = start should be stack = [start].”

---

### **Stage 2 — Fix Pipeline**

🪄 **Fix Attempt #1:** Partial success (88% pass rate)
🪄 **Fix Attempt #2:** 100% success

✅ **Final Fixed Code:**

```python
def dfs_search_v1(graph, start, target):
    """Find if target is reachable from start."""
    if graph is None:
        return False

    visited = set()
    stack = [start]

    while stack:
        current = stack.pop()
        if current == target:
            return True
        if current not in visited:
            visited.add(current)
            neighbors = graph.get(current)
            if neighbors is None:
                continue
            if not isinstance(neighbors, (list, set, tuple)):
                raise TypeError(
                    f"Graph value for node '{current}' must be iterable."
                )
            for neighbor in neighbors:
                if neighbor not in visited:
                    stack.append(neighbor)
    return False
```

---

## ☁️ Deploying to Google Cloud

### Deploy to Agent Engine

```bash
./deploy.sh agent-engine
```

### Deploy to Cloud Run (with UI)

```bash
./deploy.sh cloud-run
```

---

## 🧩 Observability with Cloud Trace

Once deployed, you can analyze:

* **Execution timelines** for each agent
* **Performance bottlenecks** (e.g., Test Runner latency)
* **Token usage and cost breakdowns**
* **Loop iterations** in the fix pipeline

---

## 🧠 Key Learnings

| Concept                 | Description                                                      |
| ----------------------- | ---------------------------------------------------------------- |
| **Tools vs Agents**     | Tools handle deterministic logic; Agents decide when to use them |
| **Sequential Pipeline** | Analyzer → Style Checker → Test Runner → Synthesizer             |
| **Loop Agent**          | Iterative code fixing until all tests pass                       |
| **State & Memory**      | State = current review, Memory = cross-session learning          |
| **Deployment**          | Agent Engine = fully managed, Cloud Run = UI-enabled             |
| **Observability**       | Cloud Trace for latency, token, and debugging insights           |

---

## 📚 Resources

* **Google ADK Docs:** [https://github.com/google/genai](https://github.com/google/genai)
* **Vertex AI Agent Engine:** [https://cloud.google.com/vertex-ai](https://cloud.google.com/vertex-ai)
* **Original Codelab:** [Building a Production AI Code Review Assistant](https://codelabs.developers.google.com/adk-code-reviewer-assistant/instructions)
