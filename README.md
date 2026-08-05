# Interview Preparation Assistant using Multi-Agent AI System

[![Technology](https://img.shields.io/badge/LangGraph-Multi--Agent-orange)](#-multi-agent-architecture)
[![Backend](https://img.shields.io/badge/FastAPI-Python_3.11-green)](#-technology-stack)
[![Frontend](https://img.shields.io/badge/React.js-Vite_5-blue)](#-technology-stack)
[![Design](https://img.shields.io/badge/UI-Dark_Glassmorphism-purple)](#-modern-frontend-redesign)
[![LLM](https://img.shields.io/badge/Groq_API-Llama_3.3_70b-purple)](#-multi-agent-architecture)

An intelligent, multi-agent artificial intelligence application designed to automate candidate interview preparation. By leveraging specialized AI agents orchestrated via **LangGraph** and powered by **Groq API (Llama 3.3-70b)**, the platform parses resumes, evaluates target job descriptions, computes ATS scores, conducts role-adaptive mock interviews (Technical, Coding, HR), evaluates candidate answers across 5 metrics, and generates downloadable PDF performance reports.

---

## 📌 Key Features & Capabilities

- 📄 **Resume Parsing & ATS Scoring**: Automatically extracts skills, experience, education, and calculates Applicant Tracking System (ATS) alignment.
- 🎯 **Job Description Analysis**: Extracts required competencies, seniority levels, and company target keywords.
- 📊 **Skill Matching & Gap Analysis**: Computes weighted match percentage and provides actionable recommendations to address skill gaps.
- 🚫 **Anti-Repetition Question Engine**: Historical user question tracking & deduplication ensures technical, coding, and HR questions **never repeat** across sessions or rounds.
- 🧪 **10 CSE Specialization Pipeline**: Automated test runner covering 10 Computer Science Engineering sub-domains (DSA, System Design, Web Dev, SQL/DBMS, OS, Networks, ML/AI, Cybersecurity, DevOps, Software Architecture).
- 🎙️ **Virtual Interview Studio**: Live interview studio with audio/speech waveform simulation, step-by-step progress tracking, code editor interface, real-time score feedback cards, and instant PDF download.
- 🎨 **Modern Dark Glassmorphism UI**: High-end dark theme aesthetic with ambient glowing indigo/violet accents, backdrop filters (`backdrop-blur-md`), micro-animations, and responsive layouts.
- 🛡️ **Comprehensive Error Handling & Resilience**: Automatic HTTP 429 LLM rate-limit backoff, 100% unique dynamic fallback generators, ReportLab document safety, and top-level React Error Boundary.

---

## 🛠️ Technology Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend** | React.js, Vite 5, Axios, React Router v6, Glassmorphism CSS System, Custom SVG Waveforms |
| **Backend** | FastAPI (Python 3.11), Uvicorn ASGI, Pydantic v2, PyJWT |
| **Database & ORM** | SQLite / MySQL 8.0+, SQLAlchemy ORM |
| **AI Framework** | LangGraph, LangChain, Groq API (`llama-3.3-70b-versatile` / `llama3-8b-8192`) |
| **PDF Generation** | ReportLab OpenSource PDF Engine |

---

## 🧠 Multi-Agent System Architecture

The application uses **8 Specialized AI Agents** operating within a LangGraph state network:

```
+-------------------+     +-------------------+     +-------------------+
| 1. Resume Agent   | --> | 2. JD Agent       | --> | 3. Skill Matcher  |
+-------------------+     +-------------------+     +-------------------+
                                                              |
                                                              v
+-------------------+     +-------------------+     +-------------------+
| 6. HR Agent       | <-- | 5. Coding Agent   | <-- | 4. Question Gen   |
+-------------------+     +-------------------+     +-------------------+
          |
          v
+-------------------+     +-------------------+
| 7. Feedback Agent | --> | 8. Report Agent   | --> [Database + PDF Report]
+-------------------+     +-------------------+
```

1. **Resume Analyzer Agent**: Extracts structured resume metadata & ATS score.
2. **Job Description Analyzer Agent**: Extracts job requirements, experience tiers, & keywords.
3. **Skill Matching Agent**: Identifies skill gaps & calculates matching percentage.
4. **Question Generator Agent**: Synthesizes candidate-tailored technical & scenario questions with anti-repetition directives.
5. **Coding Interview Agent**: Synthesizes DSA, SQL, Python, React, and FastAPI coding problems with duplicate protection.
6. **HR Interview Agent**: Synthesizes behavioral STAR and situational questions with deduplication.
7. **Feedback Agent**: Assesses candidate responses on 5 scoring axes (Technical Accuracy, Grammar, Communication, Confidence, Completeness).
8. **Report Generator Agent**: Compiles analytics and generates downloadable PDF reports.

---

## 🧪 10 CSE Pipeline Test Suite

To test the system against 10 Computer Science Engineering specializations and verify 100% question uniqueness:

```powershell
python backend/tests/test_10_cse_pipeline.py
```

*Or via PyTest:*
```powershell
python -m pytest backend/tests/test_10_cse_pipeline.py -s
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

For the complete **Software Requirements Specification (SRS)** including architecture diagrams, ER schemas, and DAG flows:

👉 **[SRS & Enterprise Architecture Specification Document](SRS_and_Architecture_Document.md)**
