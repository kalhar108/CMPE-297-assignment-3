# 🏋️‍♂️ Sports Shop Agent AI Assistant (Finn)

**Finn** is an intelligent AI shopping assistant built using **Google’s Agent Development Kit (ADK)**, **MCP Toolbox**, and **AlloyDB for PostgreSQL**.  
It understands natural language, queries a structured database, and helps users find products, view shopping lists, locate stores, and manage orders — all deployed on **Google Cloud Run**.

---

## 🧠 Overview

Finn is a sports store assistant that combines **LLM reasoning** with **database intelligence**.  
Using AlloyDB and ADK, Finn can:
- 🏃 **Search products** by description, size, or brand  
- 🛒 **Add items** to a user’s shopping list  
- 🏬 **Find nearby stores** based on user location  
- 📦 **Check order status** or update delivery methods  
- 🤝 **Authenticate** users with Google Sign-In and secure ID tokens  

---

## 🧩 System Architecture

```

Frontend (React + Google Sign-In)
↓  (Bearer ID Token)
Backend (FastAPI + ADK + Gemini)
↓  (Secure API call)
MCP Toolbox (Tool definitions + AlloyDB access)
↓  (SQL execution)
AlloyDB (Product, Store, Orders Data)

````

**Key Components:**
| Component | Description |
|------------|-------------|
| **Frontend** | Built with React + Vite, deployed on Cloud Run. Provides chat UI and Google Sign-In. |
| **Backend** | FastAPI service using Google ADK and Gemini for reasoning and tool orchestration. |
| **Toolbox** | MCP Toolbox server exposing SQL tools connected to AlloyDB. |
| **Database** | AlloyDB for PostgreSQL storing structured product and user data. |
| **Storage** | Google Cloud Storage hosting product images. |

---

## ⚙️ Tech Stack

| Layer | Technology |
|--------|-------------|
| **Frontend** | React, Vite, TailwindCSS |
| **Backend** | FastAPI, Python 3.11, Google ADK, Gemini, Vertex AI |
| **Database** | AlloyDB for PostgreSQL |
| **Auth** | Google OAuth 2.0 (ID Tokens) |
| **Cloud Services** | Cloud Run, Cloud Build, Artifact Registry, Secret Manager, Cloud Storage |
| **Containerization** | Docker |

---

## 🚀 Features

- 🔍 **Natural Language Product Search**  
  “Show me Adidas trail running shoes.”

- 🛒 **Add and View Shopping List**  
  “Add Ultra Glide, size 40, color Red to my shopping list.”

- 📦 **Order Management**  
  “Check my orders.” or “Update delivery to Express.”

- 🗺️ **Geolocation Store Search**  
  “Find stores near me.”

- 🧩 **Dynamic Tool Invocation** via MCP Toolbox  
  The ADK agent calls the right SQL tools based on user intent.

---

## 🛠️ Project Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/sports-agent-adk-mcp-alloydb.git
cd sports-agent-adk-mcp-alloydb
````

### 2️⃣ Enable Google Cloud APIs

```bash
gcloud services enable alloydb.googleapis.com \
                       compute.googleapis.com \
                       cloudresourcemanager.googleapis.com \
                       servicenetworking.googleapis.com \
                       vpcaccess.googleapis.com \
                       aiplatform.googleapis.com \
                       artifactregistry.googleapis.com \
                       cloudbuild.googleapis.com \
                       run.googleapis.com \
                       storage.googleapis.com
```

### 3️⃣ Set Project Variables

```bash
export PROJECT_ID=eminent-wording-478400-c8
export PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")
```

---

## 🗄️ Database (AlloyDB)

1. **Create AlloyDB cluster and instance**

   ```bash
   gcloud alloydb clusters create alloydb-cluster \
       --password=alloydb \
       --network=default \
       --region=us-central1 \
       --database-version=POSTGRES_16
   ```

2. **Create database and import sample data**

   ```bash
   psql -h 127.0.0.1 -U postgres
   CREATE DATABASE store;
   \c store
   \i data/store_backup.sql
   ```

---

## 🧰 MCP Toolbox Deployment

1. **Configure `src/toolbox/tools.yaml`**

   ```yaml
   authServices:
     google_signin:
       kind: google
       clientId: 49240794644-4dpl93q5vrljg8rthsda4s5kdfrdrav9.apps.googleusercontent.com
   sources:
     my-alloydb-pg-source:
       kind: alloydb-postgres
       project: eminent-wording-478400-c8
       region: us-central1
       cluster: alloydb-cluster
       instance: alloydb-inst
       database: store
       user: postgres
       password: alloydb
   ```

2. **Upload the tools.yaml as a secret**

   ```bash
   gcloud secrets create tools --data-file=tools.yaml
   ```

3. **Deploy Toolbox to Cloud Run**

   ```bash
   export IMAGE=us-central1-docker.pkg.dev/database-toolbox/toolbox/toolbox:latest
   gcloud run deploy toolbox \
       --image $IMAGE \
       --service-account toolbox-identity \
       --region us-central1 \
       --set-secrets "/app/tools.yaml=tools:latest" \
       --args="--tools_file=/app/tools.yaml","--address=0.0.0.0","--port=8080" \
       --allow-unauthenticated
   ```

---

## 🤖 Backend Deployment (ADK Agent)

1. **Build Docker Image**

   ```bash
   gcloud builds submit src/backend/ --tag us-central1-docker.pkg.dev/$PROJECT_ID/finn-agent-images/finn-agent
   ```

2. **Deploy to Cloud Run**

   ```bash
   gcloud run deploy finn-agent \
       --image us-central1-docker.pkg.dev/$PROJECT_ID/finn-agent-images/finn-agent \
       --platform managed \
       --allow-unauthenticated \
       --region us-central1 \
       --project $PROJECT_ID \
       --set-env-vars="GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_LOCATION=us-central1,GOOGLE_GENAI_USE_VERTEXAI=TRUE,TOOLBOX_URL=https://toolbox-$PROJECT_NUMBER.us-central1.run.app"
   ```

3. **Test Backend**

   ```bash
   curl -i https://finn-agent-$PROJECT_NUMBER.us-central1.run.app/test
   curl -i https://finn-agent-$PROJECT_NUMBER.us-central1.run.app/toolbox_ping
   ```

---

## 💻 Frontend Deployment

1. **Set backend URL in `src/frontend/src/pages/Home.jsx`:**

   ```js
   const BACKEND_URL = "https://finn-agent-49240794644.us-central1.run.app";
   ```

2. **Build and Deploy Frontend**

   ```bash
   gcloud builds submit src/frontend/ --tag us-central1-docker.pkg.dev/$PROJECT_ID/finn-frontend-images/finn-frontend
   gcloud run deploy finn-frontend \
       --image us-central1-docker.pkg.dev/$PROJECT_ID/finn-frontend-images/finn-frontend \
       --platform managed \
       --allow-unauthenticated \
       --region us-central1 \
       --project $PROJECT_ID
   ```

---

## 🔐 Authentication (Google Sign-In)

* Set **Authorized JavaScript Origin** in your OAuth client:

  ```
  https://finn-frontend-49240794644.us-central1.run.app
  ```
* Copy your client ID into:

  * `src/frontend/src/components/GoogleSignInButton.jsx`
  * `src/toolbox/tools.yaml` → `authServices.google_signin.clientId`

---

## 🧩 Example Queries

| User Query                                                   | Action Triggered                     |
| ------------------------------------------------------------ | ------------------------------------ |
| “Show me Nike running shoes”                                 | Calls `search-products-by-brand`     |
| “Add Ultra Glide size 40 color Red/Grey to my shopping list” | Calls `add-product-to-shopping-list` |
| “Find stores near me”                                        | Calls `find-stores-by-user`          |
| “Check my orders”                                            | Calls `check-order-status-by-user`   |
| “Update my delivery to Express Delivery”                     | Calls `update-order-delivery-method` |

---

## 🧪 Testing API Directly

**Without auth:**

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello"}' \
  https://finn-agent-49240794644.us-central1.run.app/chat
```

**With Google ID Token:**

```bash
TOKEN="<paste_token>"
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"message":"Show me Nike running shoes"}' \
  https://finn-agent-49240794644.us-central1.run.app/chat_nostream
```

---

## 🧾 Troubleshooting

| Issue                     | Fix                                                                 |
| ------------------------- | ------------------------------------------------------------------- |
| ❌ `No response from Finn` | Verify the frontend sends the Authorization header.                 |
| ⚠️ `toolbox_ping` fails   | Ensure `TOOLBOX_URL` env variable is correct on `finn-agent`.       |
| ❗ `401 Unauthorized`      | Make sure the OAuth client ID matches in Toolbox and frontend.      |
| 💡 Empty `id_token`       | Reauthorize Google Sign-In and check Authorized JavaScript Origins. |

---

## 🎥 Video Walkthrough

A full demo video walkthrough of this project is available on YouTube:

> **[Sports Shop Agent AI Assistant](https://youtu.be/qY5JN7VQNbk)**
