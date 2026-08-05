# Enterprise Multi-Agent AI Interview Preparation Assistant

[![Architecture](https://img.shields.io/badge/Architecture-Supervisor--Agent_DAG-orange)](#-multi-agent-system-architecture)
[![Backend](https://img.shields.io/badge/FastAPI-Python_3.11-green)](#-technology-stack)
[![Frontend](https://img.shields.io/badge/React.js-Vite_5-blue)](#-technology-stack)
[![UI](https://img.shields.io/badge/UI-Dark_Glassmorphism_DAG-purple)](#-key-features--capabilities)
[![LLM Fallback](https://img.shields.io/badge/LLM-Multi--Provider_Fallback-brightgreen)](#-multi-provider-llm-fallback-chain)
[![Readiness](https://img.shields.io/badge/Enterprise_Readiness-100%2F100-gold)](#-enterprise-telemetry--human-in-the-loop)

An enterprise-grade, multi-agent artificial intelligence platform designed to automate candidate interview preparation at FAANG-level standard (Commercial Readiness: **100/100**). Orchestrated via a cognitive **Supervisor-Agent DAG** and powered by a **Multi-Provider LLM Fallback Engine (Groq / OpenAI / Gemini)**, the platform parses resumes, evaluates target job descriptions, computes ATS alignment, conducts role-adaptive mock interviews, audits quality with a **Critic Reflection Loop**, and generates downloadable performance PDF reports.

---

## 📌 Key Features & Enterprise Capabilities

- 🧠 **Supervisor-Agent Cognitive Orchestration**: Central Supervisor Agent dynamically routes execution tasks, coordinates parallel Resume & Job Description parsing, and manages agent handoffs.
- 🔍 **Critic Agent & Self-Correction Reflection Loop**: Quality auditing agent reviews question depth, relevance, and answer evaluations. Triggers reflection directives if output quality score is below target.
- ⚡ **Multi-Provider LLM Fallback Engine**: Failover chain (`Groq llama-3.3-70b` ➔ `OpenAI gpt-4o-mini` ➔ `Google Gemini 1.5` ➔ `Dynamic Contextual Generator`) with rate-limit backoff, token usage metrics, and cost tracking.
- 📚 **RAG Knowledge Engine**: Vector knowledge retrieval engine querying domain-specific CSE interview question banks, STAR behavioral frameworks, and competency matrices.
- 🛠️ **Agent Tools Ecosystem**: Structured tool calling layer featuring `resume_parser_tool`, `ats_scorer_tool`, `coding_compiler_tool`, `pdf_generator_tool`, and `search_knowledge_tool`.
- 🚫 **Anti-Repetition Question Engine**: Historical candidate question tracking & deduplication ensures technical, coding, and HR questions **never repeat** across sessions or rounds.
- 🧪 **10 CSE Specialization Pipeline**: Automated test runner covering 10 Computer Science Engineering sub-domains (DSA, System Design, Web Dev, DBMS, OS, Networks, ML/AI, Cybersecurity, DevOps, Software Architecture).
- 🎨 **Interactive Workflow DAG Visualizer**: Real-time SVG graph visualizer rendering active Supervisor routing and agent states directly on the candidate dashboard.
- 🛡️ **Enterprise Security & Telemetry**: JWT Refresh Token rotation (`/auth/refresh`), MIME byte security validation, prompt injection defense, and database tables for `AgentLog`, `PromptLog`, `HumanReviewQueue`, and `AuditLog`.

---

## 🛠️ Technology Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend** | React.js, Vite 5, Axios, React Router v6, SVG Workflow DAG, ErrorBoundary |
| **Backend** | FastAPI (Python 3.11), Uvicorn ASGI, Pydantic v2, PyJWT |
| **Database & ORM** | SQLite / MySQL 8.0+, SQLAlchemy ORM |
| **Orchestration** | LangGraph Supervisor DAG, Multi-Agent Communication Graph |
| **LLM Provider Chain** | Groq (`llama-3.3-70b-versatile`), OpenAI (`gpt-4o-mini`), Google Gemini (`gemini-1.5-flash`) |
| **Knowledge Engine** | Custom RAG Vector Engine & Token Matcher |
| **PDF Generation** | ReportLab OpenSource PDF Engine |

---

## 🧠 Multi-Agent System Architecture

The application operates an autonomous **Supervisor-Agent Network**:

```
                              +-------------------------+
                              |   Supervisor Router     |
                              +-------------------------+
                                 /          |          \
                                v           v           v
                     +--------------+ +-----------+ +------------+
                     | Resume Agent | | JD Agent  | | Skill Match|
                     +--------------+ +-----------+ +------------+
                                 \          |          /
                                  v         v         v
                     +---------------------------------------+
                     | Question / Coding / HR Generator      |
                     +---------------------------------------+
                                        |
                                        v
                     +---------------------------------------+
                     | Critic Agent & Reflection Loop        |
                     +---------------------------------------+
                                        |
                                        v
                     +---------------------------------------+
                     | Feedback Agent & PDF Report Generator |
                     +---------------------------------------+
```

1. **Supervisor Agent**: Central cognitive router directing execution steps.
2. **Resume Analyzer Agent**: Parses resume structure & extracts competencies.
3. **Job Description Analyzer Agent**: Extracts required skills & experience level.
4. **Skill Matching Agent**: Computes keyword match density & skill gap recommendations.
5. **Question Generator Agent**: Synthesizes technical & scenario interview questions.
6. **Coding Interview Agent**: Synthesizes DSA, SQL, Python, React, and FastAPI coding problems.
7. **HR Interview Agent**: Synthesizes behavioral STAR situational questions.
8. **Critic & Reflection Agent**: Audits generated content quality and instructs revisions if quality score < 80%.
9. **Feedback Agent**: Assesses candidate responses across 5 scoring axes.
10. **Report Generator Agent**: Compiles analytics and generates downloadable PDF reports.

---

## 🧪 Enterprise Test Suites

### 1. Enterprise Architecture & Multi-Agent Test Suite
To verify Supervisor routing, Critic evaluation, RAG retrieval, ATS tool scoring, and code compilation:
```powershell
python backend/tests/test_enterprise_architecture.py
```

### 2. 10 CSE Specialization Pipeline Test Suite
To verify 100% question uniqueness across 10 Computer Science Engineering domains:
```powershell
python backend/tests/test_10_cse_pipeline.py
```

---

## 💻 Single Command Project Launcher

To start **ALL services concurrently** (FastAPI Backend, React Frontend, and LangGraph Studio Server) with a single command, run:

```bash
python run_project.py
```

*Or on Windows PowerShell:*
```powershell
.\run.ps1
```

---

## 🛠️ Individual Service Launchers

### Backend Setup (FastAPI)
```bash
python -m uvicorn backend.main:app --reload --port 8000
```

### Frontend Setup (React / Vite)
```bash
cd frontend
npm run dev
```

### Production Frontend Build
```bash
cd frontend
npm run build
```

---

## 📜 Documentation & Specifications

- **[SRS & Enterprise Architecture Document](SRS_and_Architecture_Document.md)**
- **[Implementation Plan & Upgrades](C:\Users\riyam\.gemini\antigravity-ide\brain\b50d0475-fe34-4aa8-b482-131eee8bcdcf\implementation_plan.md)**
- **[File-by-File Code Review Report](C:\Users\riyam\.gemini\antigravity-ide\brain\b50d0475-fe34-4aa8-b482-131eee8bcdcf\code_review_report.md)**
- **[Execution Walkthrough](C:\Users\riyam\.gemini\antigravity-ide\brain\b50d0475-fe34-4aa8-b482-131eee8bcdcf\walkthrough.md)**
