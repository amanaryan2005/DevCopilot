# 🛡️ DevSecOps Multi‑Agent AI Copilot

An event‑driven, enterprise‑grade DevSecOps copilot that automatically runs OWASP security scans, compliance checks, and architecture reviews on every Pull Request. It is built with **FastAPI**, **Celery**, **Redis**, **LangGraph**, **Qdrant**, fully containerized with **Docker** and provisioned via **Terraform**.[web:1][web:3][web:11][web:13][web:16][web:18][web:19]

---

## ✨ Features

- Automated OWASP Top 10 security checks on each PR.
- Policy‑aware PR reviews using Retrieval‑Augmented Generation (RAG) over Qdrant‑backed vectors.
- Static analysis of IaC (Terraform) and Kubernetes manifests for architectural risks.
- LangGraph‑driven multi‑agent orchestration with a supervisor agent to coordinate tools.[web:12][web:15][web:17]
- Asynchronous, scalable processing via Celery and Redis, triggered from GitHub webhooks.[web:1][web:11][web:14][web:16][web:18][web:19]
- Fully containerized with Docker and reproducible infrastructure via Terraform.

---

## 🏗️ Architecture

```text
           GitHub Pull Request Event
                        │
                        ▼
               FastAPI Webhook Service
           (validates event, enqueues job)
                        │
                        ▼
               Redis Message Broker
            (Celery task queue backend)
                        │
                        ▼
                Celery Worker Pool
                        │
     ┌──────────────────┼──────────────────┐
     ▼                  ▼                  ▼
Security Agent    RAG Policy Agent   Architecture Agent
(OWASP Top 10)   (Qdrant‑backed RAG) (IaC & K8s Review)
     │                  │                  │
     └──────────────────┼──────────────────┘
                        ▼
              LangGraph Supervisor Agent
        (coordinates tools, synthesizes report)
                        │
                        ▼
             GitHub PR Review & Status Check
        (inline comments + summary assessment)
```

---

## 🧩 Core Components

| Layer            | Technology                | Responsibility |
|-----------------|---------------------------|----------------|
| API Edge        | FastAPI                   | Receives GitHub PR webhooks and enqueues Celery tasks.[web:1][web:11][web:14][web:16] |
| Async Pipeline  | Celery + Redis            | Executes long‑running security, policy, and IaC checks.[web:1][web:11][web:18][web:19] |
| AI Orchestration| LangGraph                 | Manages multi‑agent workflows via a supervisor graph.[web:12][web:15][web:17] |
| Vector Storage  | Qdrant Vector DB          | Stores and retrieves policy and standard documents for RAG.[web:3] |
| Analysis Agents | Security / Policy / Arch  | Run OWASP scans, compliance checks, and infrastructure reviews. |
| Infra & Runtime | Docker + Terraform        | Define, build, and deploy the full stack environment.[web:16] |

---

## 🚀 Getting Started

### 1. Prerequisites

- Docker and Docker Compose installed.
- Python 3.10+ and `poetry` or `pip` (depending on your setup).
- GitHub App or Webhook configured to send `pull_request` events.

### 2. Clone and configure

```bash
git clone https://github.com/your-org/devsecops-ai-copilot.git
cd devsecops-ai-copilot

cp .env.example .env
# Edit .env with your GitHub, Redis, Qdrant, and LLM credentials
```

Key environment variables (example):

```env
GITHUB_APP_WEBHOOK_SECRET=...
GITHUB_APP_ID=...
GITHUB_PRIVATE_KEY_PATH=./certs/github-app.pem

REDIS_URL=redis://redis:6379/0
QDRANT_URL=http://qdrant:6333

OPENAI_API_KEY=...
POLICY_RAG_COLLECTION=policy-docs
```

---

## 🧪 Running the Stack (Docker)

```bash
docker compose up --build
```

This typically starts:

- `api`: FastAPI service exposing `/webhook/github`.
- `worker`: Celery worker(s) consuming tasks from Redis.
- `redis`: Message broker.
- `qdrant`: Vector database for RAG.

Check service health:

```bash
curl http://localhost:8000/health
```

---

## 🔔 GitHub Webhook Setup

1. Create a GitHub App or configure a repository webhook.
2. Set the payload URL to your public FastAPI endpoint, for example:

   `https://your-domain.com/webhook/github`

3. Select the **Pull request** event.
4. Set the webhook secret and keep it in `GITHUB_APP_WEBHOOK_SECRET`.

On each PR event, GitHub sends a payload to FastAPI, which:

- Validates the signature.
- Enqueues a Celery task with repository, branch, and diff metadata.
- Triggers agent workflows and posts results back to the PR as comments and status checks.

---

## 🤖 Multi‑Agent Workflow

The analysis is modeled as a LangGraph graph:

- **Security Agent**: Runs OWASP‑focused checks (dependencies, basic SAST, headers, etc.).
- **RAG Policy Agent**: Uses Qdrant + LLM to match changes against internal policies and standards.
- **Architecture Agent**: Inspects Terraform and Kubernetes manifests for misconfigurations and anti‑patterns.
- **Supervisor Agent**: Orchestrates the above tools, merges findings, and generates a single PR review message.

Each agent can be extended with new tools (e.g., SCA scanners, SAST tools, or CSPM APIs) without changing the rest of the system.

---

## 📦 Project Structure

```text
.
├── api/
│   ├── main.py            # FastAPI entrypoint, webhook routes
│   ├── deps.py            # Common dependencies
│   └── schemas.py         # Pydantic models for payloads
├── workers/
│   ├── tasks.py           # Celery tasks triggered by webhooks
│   └── celery_app.py      # Celery app configuration
├── agents/
│   ├── security.py        # OWASP / security agent
│   ├── policy_rag.py      # RAG policy agent (Qdrant + LLM)
│   ├── architecture.py    # IaC & K8s analysis agent
│   └── graph.py           # LangGraph supervisor and routing
├── infra/
│   ├── docker-compose.yml
│   ├── Dockerfile.api
│   ├── Dockerfile.worker
│   └── terraform/         # Terraform modules and envs
├── tests/
│   └── ...                # Unit and integration tests
└── README.md
```

---

## 🛡️ Security & Compliance

- Webhook endpoints are HMAC‑verified using the GitHub secret.
- Secrets are injected via environment variables or secret managers, not committed to Git.
- Qdrant and Redis are network‑isolated behind the internal Docker / VPC network.
- All external calls (LLM, GitHub) are audited via structured logging.

---

## 🗺️ Roadmap

- Add SAST/DAST integrations (Semgrep, OWASP ZAP, etc.).
- Add support for GitLab and Bitbucket webhooks.
- Expose a UI dashboard for historical PR security posture.
- Add per‑team policy packs and multi‑tenant support.

---

## 🤝 Contributing

1. Fork the repo.
2. Create your feature branch: `git checkout -b feat/my-feature`.
3. Commit changes: `git commit -m "feat: add my feature"`.
4. Push the branch: `git push origin feat/my-feature`.
5. Open a Pull Request.

---

## 📄 License

MIT (or update with your chosen license).
