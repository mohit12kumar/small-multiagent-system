# Software Requirements Specification (SRS) & Enterprise System Architecture
## Project: Interview Preparation Assistant using Multi-Agent AI System

---

## Executive Summary & Document Metadata

| Metadata Field | Project Specification Details |
| :--- | :--- |
| **Project Title** | Interview Preparation Assistant using Multi-Agent AI System |
| **Document Version** | 1.0.0 (Enterprise Specification & Academic Standard) |
| **Frontend Tech Stack** | React.js (v18+), Tailwind CSS, Axios, React Router v6, React Hook Form, Chart.js |
| **Backend Tech Stack** | FastAPI (Python 3.11), Uvicorn, SQLAlchemy ORM, Pydantic v2, PyJWT |
| **AI & Multi-Agent Framework**| LangGraph, Groq API (Llama 3 / Mixtral models), LangChain Prompt Templates |
| **Database & Storage** | MySQL 8.0+, File System (`uploads/resumes/`, `uploads/reports/`) |
| **Target Deployment** | Vercel (Frontend), Render / Oracle Cloud Infrastructure (Backend), Managed MySQL |

---

# Table of Contents
1. [Chapter 1 – Introduction](#chapter-1--introduction)
2. [Chapter 2 – Overall Description & User Roles](#chapter-2--overall-description--user-roles)
3. [Chapter 3 – System Features & Functional Modules](#chapter-3--system-features--functional-modules)
4. [Chapter 4 – Multi-Agent AI System Architecture](#chapter-4--multi-agent-ai-system-architecture)
5. [Chapter 5 – LangGraph Workflow & State Management](#chapter-5--langgraph-workflow--state-management)
6. [Chapter 6 – Database Design & Schema Specifications](#chapter-6--database-design--schema-specifications)
7. [Chapter 7 – REST API Specification Matrix](#chapter-7--rest-api-specification-matrix)
8. [Chapter 8 – Frontend Architecture & User Interface Design](#chapter-8--frontend-architecture--user-interface-design)
9. [Chapter 9 – Enterprise Diagram Suite (16 Diagrams)](#chapter-9--enterprise-diagram-suite-16-diagrams)
10. [Chapter 10 – Project Directory & Codebase Structure](#chapter-10--project-directory--codebase-structure)
11. [Chapter 11 – Development Roadmap & Future Enhancements](#chapter-11--development-roadmap--future-enhancements)

---

# Chapter 1 – Introduction

## 1.1 Purpose
This Software Requirements Specification (SRS) document defines the complete technical, functional, and architectural requirements for the **Interview Preparation Assistant using Multi-Agent AI System**. The system provides job seekers, students, and professionals with an intelligent, multi-agent AI environment that parses resumes, analyzes job descriptions, calculates ATS alignment scores, conducts domain-adaptive mock interviews (Technical, Coding, HR), evaluates responses across multiple qualitative dimensions, and generates actionable analytical reports.

## 1.2 Scope
The scope of this project encompasses:
- **Resume & Job Description Analysis**: Extracting structured metadata (skills, experience, education, projects, keywords) using specialized LLM agents and OCR/parsing engines.
- **ATS & Skill Matching Engine**: Computing quantitative ATS scores, identifying critical skill gaps, and providing tailored recommendation roadmaps.
- **Multi-Agent Interview Engine**: Generating dynamic, role-aligned questions across Technical, Data Structures & Algorithms (DSA), System Design, and Behavioral HR domains.
- **Multi-Metric Evaluation Engine**: Assessing candidate answers for technical accuracy, grammar, communication clarity, confidence level, and completeness.
- **Performance Analytics & Report Generation**: Delivering real-time dashboard widgets and downloadable, enterprise-grade PDF reports.
- **Role-Based Access Control**: Separate workflows and administration capabilities for **Candidates** and **System Administrators**.

## 1.3 Objectives
- **Target ATS Accuracy**: Achieve >90% precision in extracting technical skills and experience levels from standard PDF/DOCX resumes.
- **Adaptive Question Scaling**: Dynamically adapt question difficulty (Easy, Medium, Hard) based on job description seniority and real-time candidate answers.
- **Low-Latency Orchestration**: Maintain an average response time of under 3.5 seconds per multi-agent processing step using Groq API high-speed inference.
- **Comprehensive Candidate Insights**: Provide multi-metric radar charts (Technical, Grammar, Confidence, Communication) to highlight actionable growth areas.

## 1.4 Definitions, Acronyms, and Abbreviations
- **ATS**: Applicant Tracking System
- **DAG**: Directed Acyclic Graph
- **DSA**: Data Structures and Algorithms
- **JWT**: JSON Web Token
- **LLM**: Large Language Model
- **ORM**: Object-Relational Mapping (SQLAlchemy)
- **REST**: Representational State Transfer
- **SRS**: Software Requirements Specification

## 1.5 Intended Audience
This document is prepared for:
1. **Software Developers & AI Engineers**: To guide backend, frontend, and multi-agent implementation.
2. **System Architects & DevOps**: For environment provisioning, deployment pipelines, and database optimization.
3. **Project Evaluators & Stakeholders**: For auditing compliance with enterprise standards and academic project criteria.

## 1.6 Assumptions & Dependencies
- **Groq Cloud API**: Uninterrupted availability of Groq's high-speed inference endpoints for Llama 3 models.
- **Client Connectivity**: Candidate access to modern web browsers (Chrome, Edge, Firefox, Safari) with active internet connection.
- **Document Formats**: Resumes supplied in valid PDF or DOCX format under 10MB file size.

## 1.7 Constraints
- **Data Security**: Hashing of candidate credentials using bcrypt; token expiration enforced via JWT.
- **Stateless Agent State**: State transfers in LangGraph must be fully deterministic and serializable in JSON format.
- **Database Concurrency**: MySQL transaction isolation must support concurrent candidate mock sessions without deadlocks.

---

# Chapter 2 – Overall Description & User Roles

## 2.1 Product Perspective
The **Interview Preparation Assistant** operates as a modern cloud-native web application. The React frontend interacts with the FastAPI application layer via secure RESTful APIs. FastAPI orchestrates agent state graph executions powered by LangGraph and Groq LLM API, while persisting domain entities in a MySQL database.

```
+-------------------------------------------------------------------+
|                        PRESENTATION LAYER                         |
|             React.js + Tailwind CSS (Vercel Hosted)               |
+-------------------------------------------------------------------+
                                  | REST / JSON (JWT Auth)
                                  v
+-------------------------------------------------------------------+
|                         APPLICATION API                           |
|               FastAPI + Uvicorn (Render / OCI Hosted)             |
+-------------------------------------------------------------------+
        |                                           |
        v ORM                                       v State Graph
+-----------------------+               +---------------------------+
|    STORAGE LAYER      |               |  AGENT ORCHESTRATION LAYER|
|    MySQL 8.0 DB       |               | LangGraph + Groq LLM API  |
+-----------------------+               +---------------------------+
```

## 2.2 User Classes and Characteristics

### 1. Candidate (Primary User)
- **Profile**: Job seekers, university graduates, professionals preparing for technical or managerial interviews.
- **Key Capabilities**:
  - Register, authenticate, manage profile.
  - Upload resume and target job descriptions.
  - Conduct interactive mock interviews (Technical, Coding, HR).
  - Submit answers via text (and future voice integration).
  - View interactive analytical dashboards and download PDF performance reports.

### 2. Administrator (System Manager)
- **Profile**: Platform administrators, content moderators, academic instructors.
- **Key Capabilities**:
  - Monitor registered user activity and global interview metrics.
  - View aggregate system performance logs and agent execution rates.
  - Manage question banks, prompt templates, and difficulty parameters.
  - Audit candidate reports and system analytics.

## 2.3 Operating Environment
- **Client Side**: Cross-platform Web Browsers (Chrome 100+, Firefox 100+, Safari 15+, Edge 100+).
- **Server Side**: Python 3.11 runtime on Linux (Ubuntu 22.04 LTS), Uvicorn ASGI server with 4 worker processes.
- **Database**: MySQL 8.0 Community Server / Managed InnoDB instance.
- **External API Services**: Groq Inference Cloud (`llama-3.3-70b-versatile` / `llama3-8b-8192`).

---

# Chapter 3 – System Features & Functional Modules

The system comprises **12 Core Functional Modules**:

### 3.1 User Management & Authentication Module
- **Registration**: Email validation, password strength enforcement, role assignment (`Candidate` or `Admin`).
- **Authentication**: JWT token generation upon successful login; refresh token rotation.
- **Password Management**: Secure password reset flow using cryptographic reset tokens.

### 3.2 Resume Parsing Module
- **File Ingestion**: Accepts `.pdf` and `.docx` files up to 10MB.
- **Text Extraction**: Uses `PyPDF2` / `pdfplumber` / `docx2txt` with OCR fallback for image-based PDFs.
- **Entity Extraction**: Parses structured fields (Skills, Experience, Education, Projects).

### 3.3 Job Description (JD) Module
- **Ingestion**: Supports direct text entry or document upload.
- **Parsing**: Extracts required technical skills, mandatory experience years, core responsibilities, and company target keywords.

### 3.4 ATS Analysis Module
- **Scoring Engine**: Calculates overall ATS compatibility percentage (0-100%).
- **Keyword Match**: Measures exact and semantic keyword overlap between Resume and JD.
- **Formatting Audit**: Checks section header conventions and readability.

### 3.5 Skill Matching Module
- **Gap Analysis**: Identifies critical missing technical and soft skills.
- **Matching Percentage**: Computes weighted match score (Core Skills 60%, Experience 25%, Education 15%).
- **Recommendations**: Generates tailored learning topics to bridge identified gaps.

### 3.6 Question Generation Module
- **Contextual Prompting**: Synthesizes Resume + JD context to craft candidate-specific questions.
- **Adaptive Difficulty**: Categorizes questions into Easy, Medium, and Hard tiers.
- **Category Coverage**: Generates technical conceptual, project-deep-dive, and situational scenario questions.

### 3.7 Coding Interview Module
- **Domain Focus**: DSA (Array, Tree, Graph, Dynamic Programming), SQL, Python, React, FastAPI.
- **Problem Delivery**: Delivers problem statement, input/output constraints, sample test cases, and starter code snippets.

### 3.8 HR Interview Module
- **Behavioral Questions**: Uses STAR method (Situation, Task, Action, Result) templates.
- **Leadership & Situational**: Evaluates teamwork, conflict resolution, project management, and career goals.

### 3.9 Real-Time Feedback Module
- **Multi-Metric Scoring**: Evaluates candidate submissions across 5 distinct axes:
  1. *Technical Accuracy* (0-100)
  2. *Grammar & Syntax* (0-100)
  3. *Communication Clarity* (0-100)
  4. *Confidence Indicator* (0-100)
  5. *Completeness Score* (0-100)
- **Detailed Corrections**: Offers model answer benchmarks and corrective suggestions.

### 3.10 Comprehensive Report Module
- **Score Aggregation**: Computes overall interview readiness index.
- **PDF Generation**: Generates styled PDF reports with structured score tables and recommendations using ReportLab / HTML-to-PDF engines.
- **Storage**: Persists reports in `uploads/reports/` and stores reference paths in MySQL.

### 3.11 Dashboard Module
- **Real-Time Visualizations**: Powered by Chart.js in React.
- **Widgets Included**: ATS Score, Skill Match %, Technical Score, Coding Score, HR Score, Communication, Grammar, Confidence, Overall Readiness, Recent Sessions List, Weak Skills List, Recommended Topics.

### 3.12 Admin Module
- **User Management**: View user listing, toggle active/disabled states, inspect session counts.
- **Analytics & Logs**: Monitor agent request volumes, API latencies, error frequencies.
- **Prompt Management**: Live editor to update system prompts for the 8 AI agents.

---

# Chapter 4 – Multi-Agent AI System Architecture

The core intelligent layer consists of **8 Specialized AI Agents** operating as discrete nodes within a LangGraph orchestration network.

```
                     +---------------------------+
                     |    1. Resume Analyzer     |
                     +---------------------------+
                                   |
                                   v
                     +---------------------------+
                     |    2. JD Analyzer         |
                     +---------------------------+
                                   |
                                   v
                     +---------------------------+
                     |    3. Skill Match Agent   |
                     +---------------------------+
                                   |
                                   v
                     +---------------------------+
                     |    4. Question Generator  |
                     +---------------------------+
                                   |
                     +-------------+-------------+
                     |                           |
                     v                           v
      +---------------------------+ +---------------------------+
      |  5. Coding Interview Agent| |   6. HR Interview Agent   |
      +---------------------------+ +---------------------------+
                     |                           |
                     +-------------+-------------+
                                   |
                                   v
                     +---------------------------+
                     |    7. Feedback Agent      |
                     +---------------------------+
                                   |
                                   v
                     +---------------------------+
                     |    8. Report Generator    |
                     +---------------------------+
```

### Agent Detailed Specifications

| Agent Name | Input Payload | LLM Engine & Prompt Strategy | Output Payload |
| :--- | :--- | :--- | :--- |
| **1. Resume Analyzer** | Raw Resume Text / PDF File | Zero-shot structured JSON extraction via Groq | Extracted Skills, Experience, Education, Projects, ATS Base Score |
| **2. JD Analyzer** | Raw JD Text | Key-phrase extraction & Seniority classifier | Required Skills, Min Experience, Responsibilities, Company Keywords |
| **3. Skill Match Agent** | Extracted Resume JSON + JD JSON | Semantic vector similarity & set intersection | Skill Match %, Missing Skills List, Actionable Recommendations |
| **4. Question Generator** | Skill Match Output + Role Context | Few-shot role-based question synthesis | Technical Questions, Project Questions, Scenario Questions (Easy/Med/Hard) |
| **5. Coding Agent** | Target Role Domain & Seniority | Code problem generation with test cases | DSA / SQL / Python / React / FastAPI problem sets + Starter Code |
| **6. HR Agent** | Role Context + Company Profile | Behavioral STAR question framing | HR, Leadership, Teamwork, Conflict Resolution questions |
| **7. Feedback Agent** | Candidate Answer + Question + Context | Multi-criteria rubric evaluator LLM chain | Scores (Grammar, Technical, Comm, Confidence, Completeness) + Explanations |
| **8. Report Generator** | All Session Scores & Answers | Data aggregation & Markdown/HTML PDF template renderer | Final Performance PDF, Radar Chart Data, Preparation Roadmap |

---

# Chapter 5 – LangGraph Workflow & State Management

## 5.1 State Machine Schema (`InterviewState`)
In LangGraph, state is maintained in a centralized `TypedDict` passed across all agents.

```python
from typing import List, Dict, Any, Optional
from typing_extensions import TypedDict

class InterviewState(TypedDict):
    user_id: int
    session_id: int
    resume_raw_text: str
    jd_raw_text: str
    
    # Resume Analyzer Output
    resume_skills: List[str]
    resume_experience: List[Dict[str, Any]]
    resume_education: List[Dict[str, Any]]
    resume_projects: List[Dict[str, Any]]
    ats_score: float
    
    # JD Analyzer Output
    jd_skills: List[str]
    jd_experience_years: int
    jd_keywords: List[str]
    
    # Skill Match Output
    skill_match_percentage: float
    missing_skills: List[str]
    skill_recommendations: List[str]
    
    # Question Generator Outputs
    technical_questions: List[Dict[str, Any]]
    coding_questions: List[Dict[str, Any]]
    hr_questions: List[Dict[str, Any]]
    
    # User Submissions & Feedback
    current_question_index: int
    user_answers: Dict[int, str]
    question_feedbacks: Dict[int, Dict[str, Any]]
    
    # Final Report Output
    overall_readiness_score: float
    report_pdf_path: str
    is_completed: bool
```

## 5.2 Conditional Routing Logic
The LangGraph router uses a dynamic router function to direct control flow based on question types and interview state completion.

```
       START ──► [Resume Analyzer] ──► [JD Analyzer] ──► [Skill Matcher]
                                                               │
                                                               ▼
                                                      [Question Generator]
                                                               │
                                         ┌─────────────────────┴─────────────────────┐
                                         ▼                                           ▼
                              [Coding Interview Agent]                     [HR Interview Agent]
                                         │                                           │
                                         └─────────────────────┬─────────────────────┘
                                                               ▼
                                                       [User Submissions]
                                                               │
                                                               ▼
                                                        [Feedback Agent]
                                                               │
                                                               ▼
                                                       [Report Generator]
                                                               │
                                                               ▼
                                                          (Store MySQL) ──► END
```

---

# Chapter 6 – Database Design & Schema Specifications

The relational schema is implemented in **MySQL 8.0** using **SQLAlchemy ORM**.

## 6.1 Entity Relationship Summary

```
+------------+       1:N       +------------+
|   Users    |---------------->|  Resumes   |
+------------+                 +------------+
   |      |
   |1:N   |1:N
   v      v
+------------+               +------------+
|JobDescr-   |               |  Reports   |
|iptions     |               +------------+
+------------+
   |
   |1:N
   v
+-------------------+     1:N     +------------+
|InterviewSessions  |------------>| Questions  |
+-------------------+             +------------+
                                        |
                                        |1:1
                                        v
                                  +------------+     1:1     +------------+
                                  |  Answers   |------------>|  Feedback  |
                                  +------------+             +------------+
```

## 6.2 Data Tables DDL & Schema Details

### 1. `users` Table
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('candidate', 'admin') DEFAULT 'candidate',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 2. `resumes` Table
```sql
CREATE TABLE resumes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    resume_path VARCHAR(255) NOT NULL,
    skills JSON,
    education JSON,
    experience JSON,
    projects JSON,
    ats_score FLOAT DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 3. `job_descriptions` Table
```sql
CREATE TABLE job_descriptions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    description TEXT NOT NULL,
    skills JSON,
    experience_years INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 4. `interview_sessions` Table
```sql
CREATE TABLE interview_sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    jd_id INT,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    duration_minutes INT DEFAULT 0,
    status ENUM('pending', 'in_progress', 'completed') DEFAULT 'pending',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (jd_id) REFERENCES job_descriptions(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 5. `questions` Table
```sql
CREATE TABLE questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT NOT NULL,
    question_text TEXT NOT NULL,
    difficulty ENUM('easy', 'medium', 'hard') DEFAULT 'medium',
    type ENUM('technical', 'coding', 'hr', 'scenario') NOT NULL,
    FOREIGN KEY (session_id) REFERENCES interview_sessions(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 6. `answers` Table
```sql
CREATE TABLE answers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question_id INT NOT NULL UNIQUE,
    answer_text TEXT NOT NULL,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 7. `feedback` Table
```sql
CREATE TABLE feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    answer_id INT NOT NULL UNIQUE,
    grammar_score FLOAT NOT NULL,
    technical_score FLOAT NOT NULL,
    communication_score FLOAT NOT NULL,
    confidence_score FLOAT NOT NULL,
    completeness_score FLOAT NOT NULL,
    overall_score FLOAT NOT NULL,
    comments TEXT,
    FOREIGN KEY (answer_id) REFERENCES answers(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 8. `reports` Table
```sql
CREATE TABLE reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    session_id INT NOT NULL UNIQUE,
    overall_score FLOAT NOT NULL,
    pdf_path VARCHAR(255) NOT NULL,
    skill_gap_summary JSON,
    improvement_plan JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (session_id) REFERENCES interview_sessions(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

---

# Chapter 7 – REST API Specification Matrix

All backend endpoints are built using **FastAPI** with Pydantic payload validation and JWT authorization headers (`Authorization: Bearer <token>`).

| Module | HTTP Method | Endpoint Route | Request Body / Params | Response Description |
| :--- | :--- | :--- | :--- | :--- |
| **Auth** | `POST` | `/api/v1/auth/register` | `{ name, email, password, role }` | User creation confirmation + ID |
| **Auth** | `POST` | `/api/v1/auth/login` | `{ email, password }` | Access Token (JWT) + User Profile |
| **Auth** | `POST` | `/api/v1/auth/logout` | Header Token | Token blacklist confirmation |
| **Resume** | `POST` | `/api/v1/resume/upload` | Multipart `file` (.pdf/.docx) | Parsed skills, experience & ATS score |
| **Resume** | `GET` | `/api/v1/resume` | Header Token | Candidate active parsed resume |
| **Resume** | `DELETE`| `/api/v1/resume/{id}` | Path `id` | Deletion status |
| **JD** | `POST` | `/api/v1/jd/upload` | `{ description_text }` or File | Parsed JD requirements & skills |
| **JD** | `GET` | `/api/v1/jd` | Header Token | List of saved job descriptions |
| **Interview**| `POST` | `/api/v1/interview/start` | `{ resume_id, jd_id }` | Initiates LangGraph session & returns initial question batch |
| **Interview**| `POST` | `/api/v1/interview/answer`| `{ question_id, answer_text }` | Submits candidate response & triggers Feedback Agent |
| **Interview**| `GET` | `/api/v1/feedback/{answer_id}`| Path `answer_id` | Multi-metric scores & AI analysis |
| **Reports** | `GET` | `/api/v1/report/{session_id}`| Path `session_id` | Full analytical report JSON |
| **Reports** | `GET` | `/api/v1/report/{id}/pdf` | Path `id` | PDF file stream download |
| **Dashboard**| `GET` | `/api/v1/dashboard` | Header Token | Aggregated scores, session history, radar metrics |
| **Admin** | `GET` | `/api/v1/admin/users` | Admin JWT Header | All users list with activity status |
| **Admin** | `GET` | `/api/v1/admin/analytics` | Admin JWT Header | System-wide LLM token usage & session metrics |

---

# Chapter 8 – Frontend Architecture & User Interface Design

## 8.1 Page Routing Layout (12 Frontend Pages)
The React application utilizes `react-router-dom` v6 with protected route wrappers for Candidates and Admins.

```
/ (Landing Page)
├── /register (Candidate & Admin Registration)
├── /login (Authentication)
├── /dashboard (Candidate Main Analytics Hub)
├── /resume-upload (Resume Processing Interface)
├── /jd-upload (Job Description Parsing Interface)
├── /interview (Interactive Mock Interview Session)
├── /coding-practice (IDE-Style Coding Environment)
├── /feedback (Instant Real-time Answer Feedback)
├── /reports (Historical Session Reports & PDF Download)
├── /profile (User Settings & Resume Management)
├── /settings (Theme, Preferences & Security)
└── /admin (Admin Control Dashboard & System Logs)
```

## 8.2 Dashboard Widgets Specification (12 Core Widgets)
1. **Resume ATS Score Widget**: Gauge meter showing 0-100% ATS score.
2. **Skill Match % Widget**: Circular progress indicator comparing candidate vs. JD skills.
3. **Technical Score Widget**: Progress bar evaluating technical question accuracy.
4. **Coding Score Widget**: Score metric evaluating algorithm problem performance.
5. **HR Score Widget**: Score metric for behavioral & soft skills.
6. **Communication Score Widget**: Text clarity indicator.
7. **Grammar Score Widget**: Grammar correctness rating.
8. **Confidence Score Widget**: Sentiment and tone rating.
9. **Overall Readiness Index**: Aggregated composite score for target role readiness.
10. **Recent Sessions List**: Table displaying past mock interview dates, roles, and scores.
11. **Weak Skills Badge List**: Tag cloud highlighting missing technical domains.
12. **Recommended Topics List**: Interactive roadmap suggestions.

---

# Chapter 9 – Enterprise Diagram Suite (16 Diagrams)

### 9.1 System Architecture Diagram
```mermaid
graph TB
    subgraph Client_Layer ["Presentation Layer (Vercel)"]
        UI["React.js Single Page App"]
        TW["Tailwind CSS Styling"]
        CJ["Chart.js Analytics"]
        UI --- TW
        UI --- CJ
    end

    subgraph API_Layer ["Application Layer (Render / OCI)"]
        GW["FastAPI Gateway / Uvicorn"]
        JWT["JWT Auth Middleware"]
        PYD["Pydantic Data Validators"]
        GW --- JWT
        GW --- PYD
    end

    subgraph Agent_Layer ["Multi-Agent Orchestration Layer"]
        LG["LangGraph Engine"]
        RA["Resume Agent"]
        JA["JD Agent"]
        SMA["Skill Match Agent"]
        QG["Question Generator"]
        CA["Coding Agent"]
        HRA["HR Agent"]
        FA["Feedback Agent"]
        RGA["Report Generator"]

        LG --> RA & JA & SMA & QG & CA & HRA & FA & RGA
    end

    subgraph External_Services ["External Cloud Services"]
        GROQ["Groq LLM API (Llama 3 70B)"]
    end

    subgraph Storage_Layer ["Data & File Storage"]
        DB[(MySQL 8.0 Database)]
        FS["File Storage (uploads/)"]
    end

    Client_Layer -- "HTTPS / REST API" --> API_Layer
    API_Layer -- "Orchestrates State" --> Agent_Layer
    Agent_Layer -- "High-Speed Inference" --> External_Services
    API_Layer -- "SQLAlchemy ORM" --> Storage_Layer
```

### 9.2 Multi-Agent Architecture Diagram
```mermaid
graph TD
    State["Centralized LangGraph State (InterviewState)"]

    subgraph PreInterview ["Stage 1: Profile & Target Parsing"]
        A1["Agent 1: Resume Analyzer"]
        A2["Agent 2: JD Analyzer"]
        A3["Agent 3: Skill Matching Agent"]
        A1 -->|Resume Json| State
        A2 -->|JD Json| State
        State --> A3
    end

    subgraph QuestionGen ["Stage 2: Adaptive Question Generation"]
        A4["Agent 4: Question Generator"]
        A5["Agent 5: Coding Interview Agent"]
        A6["Agent 6: HR Interview Agent"]
        A3 -->|Match Analysis| A4
        A4 --> A5 & A6
        A5 & A6 -->|Question Sets| State
    end

    subgraph Evaluation ["Stage 3: Answer Assessment & Reporting"]
        A7["Agent 7: Feedback Agent"]
        A8["Agent 8: Report Generator Agent"]
        State -->|User Submissions| A7
        A7 -->|Multi-Metric Feedback| State
        State --> A8
    end

    A8 -->|Final PDF & DB Records| DB[(MySQL Storage)]
```

### 9.3 LangGraph Workflow Diagram
```mermaid
stateDiagram-v2
    [*] --> START
    START --> Upload_Resume
    Upload_Resume --> Resume_Analyzer_Node
    Resume_Analyzer_Node --> Upload_JD
    Upload_JD --> JD_Analyzer_Node
    JD_Analyzer_Node --> Skill_Matching_Node
    Skill_Matching_Node --> Question_Generator_Node
    
    state Question_Branching {
        [*] --> Route_Check
        Route_Check --> Coding_Agent_Node : Type == Coding
        Route_Check --> HR_Agent_Node : Type == HR / Technical
    }
    
    Question_Generator_Node --> Question_Branching
    Coding_Agent_Node --> Collect_User_Answers
    HR_Agent_Node --> Collect_User_Answers
    
    Collect_User_Answers --> Feedback_Agent_Node
    Feedback_Agent_Node --> Check_More_Questions
    Check_More_Questions --> Question_Branching : Has Next Question
    Check_More_Questions --> Report_Generator_Node : All Answered
    
    Report_Generator_Node --> Store_MySQL
    Store_MySQL --> END
    END --> [*]
```

### 9.4 Use Case Diagram
```mermaid
graph LR
    Candidate((Candidate User))
    Admin((Admin User))

    subgraph SystemBoundary ["Interview Preparation Assistant Boundary"]
        UC1["Register & Authenticate"]
        UC2["Upload Resume"]
        UC3["Upload Job Description"]
        UC4["View ATS Score & Skill Gaps"]
        UC5["Start Mock Interview Session"]
        UC6["Submit Technical & HR Answers"]
        UC7["Solve Coding Problems"]
        UC8["View Real-time Answer Feedback"]
        UC9["Download PDF Report"]
        
        UC10["Manage Users & Roles"]
        UC11["View System Analytics"]
        UC12["Manage Question Banks & Prompts"]
    end

    Candidate --> UC1
    Candidate --> UC2
    Candidate --> UC3
    Candidate --> UC4
    Candidate --> UC5
    Candidate --> UC6
    Candidate --> UC7
    Candidate --> UC8
    Candidate --> UC9

    Admin --> UC1
    Admin --> UC10
    Admin --> UC11
    Admin --> UC12
```

### 9.5 Class Diagram
```mermaid
classDiagram
    class User {
        +int id
        +string name
        +string email
        +string password_hash
        +string role
        +datetime created_at
        +register()
        +login()
    }

    class Resume {
        +int id
        +int user_id
        +string resume_path
        +list skills
        +list experience
        +list education
        +float ats_score
        +parse()
    }

    class JobDescription {
        +int id
        +int user_id
        +string description
        +list skills
        +int experience_years
        +extract_requirements()
    }

    class InterviewSession {
        +int id
        +int user_id
        +int jd_id
        +string status
        +datetime date
        +start_session()
        +end_session()
    }

    class Question {
        +int id
        +int session_id
        +string question_text
        +string difficulty
        +string type
    }

    class Answer {
        +int id
        +int question_id
        +string answer_text
        +datetime submitted_at
    }

    class Feedback {
        +int id
        +int answer_id
        +float grammar_score
        +float technical_score
        +float communication_score
        +float confidence_score
        +float completeness_score
        +float overall_score
        +string comments
    }

    class Report {
        +int id
        +int user_id
        +int session_id
        +float overall_score
        +string pdf_path
        +generate_pdf()
    }

    User "1" -- "N" Resume
    User "1" -- "N" JobDescription
    User "1" -- "N" InterviewSession
    InterviewSession "1" -- "N" Question
    Question "1" -- "1" Answer
    Answer "1" -- "1" Feedback
    User "1" -- "N" Report
    InterviewSession "1" -- "1" Report
```

### 9.6 Entity Relationship (ER) Diagram
```mermaid
erDiagram
    USERS ||--o{ RESUMES : uploads
    USERS ||--o{ JOB_DESCRIPTIONS : submits
    USERS ||--o{ INTERVIEW_SESSIONS : conducts
    USERS ||--o{ REPORTS : receives
    JOB_DESCRIPTIONS ||--o{ INTERVIEW_SESSIONS : targets
    INTERVIEW_SESSIONS ||--o{ QUESTIONS : contains
    QUESTIONS ||--|| ANSWERS : yields
    ANSWERS ||--|| FEEDBACK : evaluates
    INTERVIEW_SESSIONS ||--|| REPORTS : generates

    USERS {
        int id PK
        string name
        string email
        string password
        string role
        timestamp created_at
    }

    RESUMES {
        int id PK
        int user_id FK
        string resume_path
        json skills
        json education
        json experience
        float ats_score
    }

    JOB_DESCRIPTIONS {
        int id PK
        int user_id FK
        text description
        json skills
        int experience_years
    }

    INTERVIEW_SESSIONS {
        int id PK
        int user_id FK
        int jd_id FK
        string status
        timestamp date
    }

    QUESTIONS {
        int id PK
        int session_id FK
        text question_text
        string difficulty
        string type
    }

    ANSWERS {
        int id PK
        int question_id FK
        text answer_text
        timestamp submitted_at
    }

    FEEDBACK {
        int id PK
        int answer_id FK
        float grammar_score
        float technical_score
        float communication_score
        float confidence_score
        float overall_score
    }

    REPORTS {
        int id PK
        int user_id FK
        int session_id FK
        float overall_score
        string pdf_path
    }
```

### 9.7 Sequence Diagram
```mermaid
sequenceDiagram
    autonumber
    actor Candidate
    participant ReactUI as React Frontend
    participant FastAPI as FastAPI Backend
    participant Graph as LangGraph Orchestrator
    participant Groq as Groq LLM API
    participant DB as MySQL Database

    Candidate->>ReactUI: Upload Resume & Job Description
    ReactUI->>FastAPI: POST /api/v1/resume/upload & POST /api/v1/jd/upload
    FastAPI->>Graph: Initialize InterviewState(user_id, resume, jd)
    Graph->>Groq: Resume Analyzer Agent (Extract metadata)
    Groq-->>Graph: Return Skills, Experience & ATS Score
    Graph->>Groq: JD Analyzer Agent (Extract requirements)
    Groq-->>Graph: Return Required Skills & Seniority
    Graph->>Groq: Skill Match Agent (Compute gap analysis)
    Groq-->>Graph: Skill Gap & Match Percentage
    Graph-->>FastAPI: Return ATS & Skill Match Summary
    FastAPI-->>ReactUI: Display ATS Score & Matching Dashboard

    Candidate->>ReactUI: Click "Start Interview"
    ReactUI->>FastAPI: POST /api/v1/interview/start
    FastAPI->>Graph: Trigger Question Generator Node
    Graph->>Groq: Generate Technical & HR Questions
    Groq-->>Graph: Return Question Set
    Graph-->>FastAPI: Return First Question Payload
    FastAPI-->>ReactUI: Render Question Page

    Candidate->>ReactUI: Submit Answer Text
    ReactUI->>FastAPI: POST /api/v1/interview/answer
    FastAPI->>Graph: Trigger Feedback Agent Node
    Graph->>Groq: Analyze Technical, Grammar, Confidence
    Groq-->>Graph: Return Multi-Metric Feedback
    Graph->>DB: Store Answer & Feedback Records
    Graph-->>FastAPI: Return Real-time Feedback
    FastAPI-->>ReactUI: Render Feedback & Next Question Button

    Candidate->>ReactUI: Complete Final Question
    FastAPI->>Graph: Trigger Report Generator Node
    Graph->>DB: Compile Session Metrics & Store PDF Report
    Graph-->>FastAPI: Return Report Download URL
    FastAPI-->>ReactUI: Render Final Dashboard & PDF Download Link
```

### 9.8 Activity Diagram
```mermaid
graph TD
    A([Start User Action]) --> B{User Registered?}
    B -- No --> C[Fill Registration Form]
    C --> D[Submit Credentials]
    D --> E[Login to Account]
    B -- Yes --> E
    E --> F[Access Dashboard]
    F --> G[Upload Resume File]
    G --> H[Parse Resume Skills & ATS Score]
    H --> I[Upload Target Job Description]
    I --> J[Run Skill Match Agent]
    J --> K[View Skill Match % & Gaps]
    K --> L{Proceed to Mock Interview?}
    L -- No --> F
    L -- Yes --> M[Select Domains: Technical, Coding, HR]
    M --> N[Initialize LangGraph Session]
    N --> O[Display Dynamic Question]
    O --> P[Candidate Inputs Response]
    P --> Q[Execute Feedback Agent LLM Chain]
    Q --> R[Display Multi-Metric Scores]
    R --> S{More Questions Remaining?}
    S -- Yes --> O
    S -- No --> T[Compile Performance Metrics]
    T --> U[Generate PDF Report]
    U --> V[Save to MySQL Database]
    V --> W[Display Final Report & Download Link]
    W --> X([End Workflow])
```

### 9.9 Component Diagram
```mermaid
graph TB
    subgraph Frontend_Component ["React Frontend Component Bundle"]
        AuthComp["Auth Component (Login/Register)"]
        DashComp["Dashboard Visualizer Component"]
        ResComp["Resume/JD Upload Component"]
        IntComp["Interactive Interview Runner"]
        RepComp["Report & PDF Viewer Component"]
    end

    subgraph Backend_Component ["FastAPI Server Modules"]
        APIRouter["API Gateway Router"]
        JWTService["Security & Auth Middleware"]
        AgentOrchestrator["LangGraph Workflow Engine"]
        PDFEngine["ReportLab PDF Generator"]
        DBConnector["SQLAlchemy Database Manager"]
    end

    subgraph External_Services ["External Infrastructure"]
        GroqService["Groq Cloud LLM Service"]
        MySQLStore["MySQL Database Storage"]
    end

    AuthComp --> APIRouter
    DashComp --> APIRouter
    ResComp --> APIRouter
    IntComp --> APIRouter
    RepComp --> APIRouter

    APIRouter --> JWTService
    APIRouter --> AgentOrchestrator
    APIRouter --> PDFEngine
    APIRouter --> DBConnector

    AgentOrchestrator --> GroqService
    DBConnector --> MySQLStore
```

### 9.10 Deployment Diagram
```mermaid
graph TB
    subgraph Client_Browser ["Candidate Workstation"]
        Browser["Modern Web Browser (Chrome/Firefox/Edge)"]
    end

    subgraph Vercel_Cloud ["Vercel Edge Network (Frontend)"]
        CDN["Vercel CDN"]
        ReactApp["Built Static React Asset Bundle"]
        CDN --- ReactApp
    end

    subgraph Backend_Cloud ["Render / Oracle Cloud (Backend API)"]
        LB["Load Balancer / Nginx"]
        DockerContainer["Docker Container (Python 3.11 + FastAPI)"]
        UvicornWorkers["Uvicorn ASGI Workers (4 Process Threads)"]
        LB --- DockerContainer
        DockerContainer --- UvicornWorkers
    end

    subgraph Database_Cloud ["Managed Database Cluster"]
        MySQLServer["MySQL 8.0 Server Instance (InnoDB Engine)"]
    end

    subgraph AI_Cloud ["Groq Cloud Platform"]
        GroqCluster["Groq LPU Processing Units (Llama 3 70B)"]
    end

    Browser -- "HTTPS (TLS 1.3)" --> CDN
    Browser -- "REST / WSS API" --> LB
    UvicornWorkers -- "Encrypted MySQL Connection (Port 3306)" --> MySQLServer
    UvicornWorkers -- "HTTPS REST API (Groq API Key)" --> GroqCluster
```

### 9.11 Data Flow Diagram (Level 0 - Context Diagram)
```mermaid
graph TD
    User["Candidate / User"]
    Admin["System Administrator"]
    System["Interview Preparation Assistant (Multi-Agent System)"]
    Groq["Groq LLM Service"]
    DB[(MySQL Database)]

    User -- "1. Upload Credentials, Resume & JD" --> System
    User -- "2. Submit Interview Answers" --> System
    System -- "3. Deliver ATS Scores, Questions & Feedback" --> User
    System -- "4. Provide Final PDF Report & Dashboard" --> User

    Admin -- "5. Prompt & System Configuration" --> System
    System -- "6. Send Analytics & Audit Logs" --> Admin

    System -- "7. Send Context Prompts" --> Groq
    Groq -- "8. Return Model Outputs" --> System

    System <--> DB
```

### 9.12 Data Flow Diagram (Level 1)
```mermaid
graph TD
    User["Candidate"]
    P1["1.0 Auth Process"]
    P2["2.0 Resume & JD Parsing"]
    P3["3.0 Skill Match & ATS Scoring"]
    P4["4.0 Multi-Agent Question Generation"]
    P5["5.0 Answer Evaluation"]
    P6["6.0 Report Compilation"]

    D1[("D1: Users Store")]
    D2[("D2: Resumes & JDs Store")]
    D3[("D3: Questions & Answers Store")]
    D4[("D4: Reports & Feedback Store")]

    User -->|Credentials| P1
    P1 -->|Write User| D1
    P1 -->|Issue JWT Token| User

    User -->|Resume & JD Files| P2
    P2 -->|Save Parsed Data| D2
    
    D2 -->|Resume & JD JSON| P3
    P3 -->|ATS Score & Skill Gap| User

    P3 -->|Skill Match Data| P4
    P4 -->|Write Questions| D3
    P4 -->|Deliver Questions| User

    User -->|Submit Answers| P5
    P5 -->|Write Answers & Feedback| D3
    P5 -->|Write Feedback Metrics| D4

    D4 -->|Aggregate Session Data| P6
    P6 -->|Write Report Path| D4
    P6 -->|Deliver PDF & Analytics| User
```

### 9.13 API Flow Diagram
```mermaid
graph LR
    Client["React UI Client"]
    Router["FastAPI Router (`api/interview.py`)"]
    Auth["JWT Guard Middleware"]
    GraphEngine["LangGraph State Engine"]
    Agents["Agent Pipeline (1-8)"]
    GroqAPI["Groq LLM Service"]
    ORM["SQLAlchemy ORM"]
    DB[(MySQL Database)]

    Client -->|1. HTTP POST Request| Router
    Router -->|2. Validate Token| Auth
    Auth -->|3. Authorized| Router
    Router -->|4. Invoke Workflow| GraphEngine
    GraphEngine -->|5. Execute Node| Agents
    Agents -->|6. API Inference| GroqAPI
    GroqAPI -->|7. Return Completion| Agents
    Agents -->|8. Update State| GraphEngine
    GraphEngine -->|9. Persist Entity| ORM
    ORM -->|10. SQL Commit| DB
    GraphEngine -->|11. Return Output| Router
    Router -->|12. JSON Response| Client
```

### 9.14 Database Schema Diagram
```mermaid
erDiagram
    users {
        int id PK
        string name
        string email
        string password
        enum role
        timestamp created_at
    }

    resumes {
        int id PK
        int user_id FK
        string resume_path
        json skills
        json education
        json experience
        json projects
        float ats_score
        timestamp created_at
    }

    job_descriptions {
        int id PK
        int user_id FK
        text description
        json skills
        int experience_years
        timestamp created_at
    }

    interview_sessions {
        int id PK
        int user_id FK
        int jd_id FK
        timestamp date
        int duration_minutes
        enum status
    }

    questions {
        int id PK
        int session_id FK
        text question_text
        enum difficulty
        enum type
    }

    answers {
        int id PK
        int question_id FK
        text answer_text
        timestamp submitted_at
    }

    feedback {
        int id PK
        int answer_id FK
        float grammar_score
        float technical_score
        float communication_score
        float confidence_score
        float completeness_score
        float overall_score
        text comments
    }

    reports {
        int id PK
        int user_id FK
        int session_id FK
        float overall_score
        string pdf_path
        json skill_gap_summary
        json improvement_plan
        timestamp created_at
    }

    users ||--o{ resumes : ""
    users ||--o{ job_descriptions : ""
    users ||--o{ interview_sessions : ""
    users ||--o{ reports : ""
    job_descriptions ||--o{ interview_sessions : ""
    interview_sessions ||--o{ questions : ""
    questions ||--|| answers : ""
    answers ||--|| feedback : ""
    interview_sessions ||--|| reports : ""
```

### 9.15 Agent Communication Diagram
```mermaid
graph TD
    subgraph Message_Payloads ["Agent Inter-Communication State Directory"]
        S1["Resume Data Payload: {skills, experience, education, projects}"]
        S2["JD Data Payload: {required_skills, exp_years, keywords}"]
        S3["Skill Match Payload: {match_percentage, missing_skills, recommendations}"]
        S4["Question Set Payload: {technical_q, coding_q, hr_q}"]
        S5["Feedback Payload: {technical_score, grammar_score, comm_score, confidence_score}"]
    end

    A1["Resume Analyzer"] -->|Generates S1| S1
    A2["JD Analyzer"] -->|Generates S2| S2
    S1 & S2 -->|Consumed By| A3["Skill Match Agent"]
    A3 -->|Generates S3| S3
    S3 -->|Consumed By| A4["Question Generator"]
    A4 -->|Generates S4| S4
    S4 -->|Inputs to Candidate &| A7["Feedback Agent"]
    A7 -->|Generates S5| S5
    S1 & S2 & S3 & S4 & S5 -->|Consolidated In| A8["Report Generator"]
```

### 9.16 Folder Structure Diagram
```mermaid
graph TD
    Root["InterviewPreparationAssistant/"]
    
    subgraph Backend_Tree ["backend/ Directory"]
        B_Agents["agents/ (resume_agent.py, jd_agent.py, skill_match_agent.py...)"]
        B_Graph["graph/ (state.py, nodes.py, workflow.py, router.py)"]
        B_API["api/ (auth.py, resume.py, jd.py, interview.py, report.py)"]
        B_DB["database/ (connection.py, models.py)"]
        B_Prompts["prompts/ (agent_prompts.py)"]
        B_Services["services/ (pdf_service.py, ocr_service.py)"]
        B_Uploads["uploads/ (resumes/, reports/)"]
        B_Main["main.py & config.py & requirements.txt"]
    end

    subgraph Frontend_Tree ["frontend/ Directory"]
        F_Pages["pages/ (Landing, Register, Login, Dashboard, Interview...)"]
        F_Comp["components/ (Navbar, Sidebar, Widgets, QuestionCard...)"]
        F_Services["services/ (api.js, authService.js)"]
        F_Hooks["hooks/ (useAuth.js, useInterview.js)"]
        F_Context["context/ (AuthContext.jsx, InterviewContext.jsx)"]
        F_Routes["routes/ (AppRoutes.jsx, ProtectedRoute.jsx)"]
        F_App["App.jsx & index.css & package.json"]
    end

    subgraph Docs_Tree ["docs/ & Config"]
        Docs["SRS_and_Architecture_Document.md & README.md"]
    end

    Root --> Backend_Tree
    Root --> Frontend_Tree
    Root --> Docs_Tree
```

---

# Chapter 10 – Project Directory & Codebase Structure

```
InterviewPreparationAssistant/
│
├── backend/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── resume_agent.py          # Agent 1: Resume parsing & ATS calculation
│   │   ├── jd_agent.py              # Agent 2: JD requirement extraction
│   │   ├── skill_match_agent.py     # Agent 3: Skill gap & match % computation
│   │   ├── question_agent.py        # Agent 4: Technical & scenario question gen
│   │   ├── coding_agent.py          # Agent 5: DSA, SQL & code problem synthesis
│   │   ├── hr_agent.py              # Agent 6: Behavioral STAR question generator
│   │   ├── feedback_agent.py        # Agent 7: Multi-metric answer evaluator
│   │   └── report_agent.py          # Agent 8: Analytics & PDF report generator
│   │
│   ├── graph/
│   │   ├── __init__.py
│   │   ├── state.py                 # LangGraph TypedDict state schema
│   │   ├── nodes.py                 # Agent node wrappers
│   │   ├── workflow.py              # Graph compilation & execution graph
│   │   └── router.py                # Conditional routing logic functions
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py                  # Register, Login, Logout endpoints
│   │   ├── resume.py                # Upload & fetch parsed resume endpoints
│   │   ├── jd.py                    # Upload & fetch job description endpoints
│   │   ├── interview.py             # Start session, submit answer endpoints
│   │   └── report.py                # Fetch feedback & PDF download endpoints
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py            # MySQL SQLAlchemy engine & session maker
│   │   └── models.py                # Declarative ORM models (Users, Resumes, etc.)
│   │
│   ├── prompts/
│   │   └── agent_prompts.py         # System prompt templates for 8 agents
│   │
│   ├── services/
│   │   ├── pdf_service.py           # ReportLab PDF report generation
│   │   └── ocr_service.py           # PyPDF2 & text extraction engine
│   │
│   ├── uploads/
│   │   ├── resumes/                 # Uploaded candidate PDF/DOCX resumes
│   │   └── reports/                 # Generated session PDF reports
│   │
│   ├── tests/
│   │   ├── test_agents.py           # Agent unit tests
│   │   └── test_api.py              # FastAPI endpoint integration tests
│   │
│   ├── config.py                    # Environment variables (Groq Key, DB URI, JWT Secret)
│   ├── requirements.txt             # Python dependencies
│   └── main.py                      # FastAPI application entry point
│
├── frontend/
│   ├── src/
│   │   ├── assets/                  # Icons, images, logos
│   │   ├── components/              # Shared UI components (Navbar, Sidebar, Cards)
│   │   ├── context/                 # React Context (AuthContext, InterviewContext)
│   │   ├── hooks/                   # Custom hooks (useAuth, useInterview)
│   │   ├── layouts/                 # Page layout wrappers (DashboardLayout)
│   │   ├── pages/                   # 12 Page components (Dashboard, Interview...)
│   │   ├── routes/                  # Protected & public routing definitions
│   │   ├── services/                # Axios API services
│   │   ├── App.jsx                  # Main application component
│   │   └── index.css                # Tailwind CSS imports & custom styles
│   │
│   ├── package.json                 # Frontend dependencies
│   └── tailwind.config.js           # Tailwind CSS configuration
│
├── docs/
│   └── SRS_and_Architecture_Document.md
│
└── README.md                        # Master repository README
```

---

# Chapter 11 – Development Roadmap & Future Enhancements

## 11.1 Recommended Development Phases

```
Phase 1: Foundation & Authentication (Week 1-2)
  ├── MySQL schema setup & SQLAlchemy ORM creation
  ├── FastAPI JWT authentication endpoints (/register, /login)
  └── React authentication pages & AuthContext integration

Phase 2: Resume & Job Description Processing (Week 3)
  ├── Resume parsing service (PyPDF2 + OCR fallback)
  ├── Agent 1 (Resume Analyzer) & Agent 2 (JD Analyzer) implementation
  └── Resume & JD upload UI components

Phase 3: ATS Engine & Skill Matcher (Week 4)
  ├── Agent 3 (Skill Match Agent) implementation
  ├── Matching score & gap calculation logic
  └── Dashboard widget integration (ATS Score, Skill Match %)

Phase 4: Multi-Agent Interview Engine (Week 5-6)
  ├── Agent 4 (Question Generator), Agent 5 (Coding), Agent 6 (HR)
  ├── LangGraph workflow compilation (`graph/workflow.py`)
  └── Interactive mock interview UI runner component

Phase 5: Evaluation & Report Generator (Week 7)
  ├── Agent 7 (Feedback Agent) multi-metric evaluation
  ├── Agent 8 (Report Generator) & ReportLab PDF engine
  └── Feedback modal & PDF download implementation

Phase 6: Dashboard Analytics & Production Deployment (Week 8)
  ├── Chart.js integration for candidate radar charts
  ├── Admin dashboard & prompt management view
  └── Docker containerization, Vercel frontend & Render backend deployment
```

## 11.2 Future System Enhancements
1. **Voice-Based Mock Interviews**: Speech-to-text (Whisper API) and text-to-speech for real-time conversational audio interviews.
2. **Webcam Video & Emotion Analysis**: Computer vision analysis measuring candidate eye contact, posture, and facial confidence signals.
3. **Company-Specific Interview Packs**: Custom interview tracks pre-tuned for Google, Microsoft, Amazon, TCS, Infosys, and Meta interview patterns.
4. **Real-Time Collaborative Mentorship**: Live multi-user websocket rooms for human mentor co-interviewing.
5. **Integrated Online Code Compiler**: Sandbox code execution engine (Docker containerized) supporting Python, JS, C++, Java test runner execution.
6. **AI Personalized Learning Roadmaps**: Dynamic integration with online learning platforms (Coursera, Udemy, YouTube) for missing skill remediation.
7. **Interview Analytics & Skill Trends**: Long-term longitudinal progress tracking across multiple mock sessions over time.
8. **Multi-Language Support**: Support for interviewing in Spanish, French, German, Hindi, and Mandarin.
9. **Automated Reminders & Scheduling**: Calendar sync (Google Calendar / Outlook) with automated preparation reminders.
10. **LinkedIn & Job Portal Integration**: Auto-importing job descriptions directly via job URL or LinkedIn job ID.

---
*End of Software Requirements Specification & Architecture Document.*
