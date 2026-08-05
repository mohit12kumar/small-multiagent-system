import os
import sys
import time
from typing import Dict, Any, List

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from backend.graph.workflow import interview_graph
from backend.graph.nodes import generate_report_node
from backend.agents.feedback_agent import feedback_agent

CSE_TEST_CASES = [
    {
        "id": 1,
        "domain": "Data Structures & Algorithms",
        "candidate_name": "Alex Mercer (DSA Engineer)",
        "jd_text": "Role: Senior DSA Engineer. Skills Required: Python, C++, Dynamic Programming, Binary Trees, Graph Algorithms, Big-O Analysis, Memory Optimization.",
        "resume_text": "Alex Mercer - DSA Specialist. Skills: Python, C++, Dynamic Programming, Trees, Graphs, Heap, Binary Search, Time Complexity Analysis.",
        "role_title": "Senior DSA Engineer"
    },
    {
        "id": 2,
        "domain": "System Design & Distributed Systems",
        "candidate_name": "Beatrix Vance (System Architect)",
        "jd_text": "Role: Principal Distributed Systems Architect. Skills Required: Microservices, Redis, Kafka, Cassandra, Distributed Caching, Load Balancing, Database Sharding.",
        "resume_text": "Beatrix Vance - Architect. Skills: Microservices, Distributed Systems, Redis, Kafka, Cassandra, Load Balancers, Message Queues.",
        "role_title": "Principal System Architect"
    },
    {
        "id": 3,
        "domain": "Full-Stack Web Development",
        "candidate_name": "Charlie Cole (Full Stack Dev)",
        "jd_text": "Role: Full Stack Lead Engineer. Skills Required: React 18, TypeScript, FastAPI, Node.js, HTML5, Modern CSS, REST APIs, WebSockets.",
        "resume_text": "Charlie Cole - Full Stack Developer. Skills: React, JavaScript, FastAPI, Node.js, HTML5, CSS3, REST APIs, GraphQL.",
        "role_title": "Full Stack Lead Engineer"
    },
    {
        "id": 4,
        "domain": "Database Systems & SQL",
        "candidate_name": "Diana Prince (Database Engineer)",
        "jd_text": "Role: Senior Database Architect. Skills Required: PostgreSQL, MySQL, Query Optimization, B-Tree Indexing, ACID Transactions, Database Replication, NoSQL.",
        "resume_text": "Diana Prince - Database Specialist. Skills: PostgreSQL, MySQL, SQL Optimization, B-Tree Indexing, ACID Transactions, Schema Design.",
        "role_title": "Senior Database Architect"
    },
    {
        "id": 5,
        "domain": "Operating Systems & Low-Level Engineering",
        "candidate_name": "Ethan Hunt (Systems Engineer)",
        "jd_text": "Role: Systems Software Engineer. Skills Required: C, Linux Kernel, Thread Concurrency, Memory Allocation, POSIX, Inter-Process Communication, GDB.",
        "resume_text": "Ethan Hunt - Low Level Engineer. Skills: C, C++, Linux Kernel, Multithreading, Memory Management, POSIX, Assembly.",
        "role_title": "Systems Software Engineer"
    },
    {
        "id": 6,
        "domain": "Computer Networks & Architecture",
        "candidate_name": "Fiona Gallagher (Network Architect)",
        "jd_text": "Role: Network Infrastructure Architect. Skills Required: TCP/IP, Socket Programming, TLS/SSL, OAuth2, Wireshark, HTTP/3, Microservice Gateway.",
        "resume_text": "Fiona Gallagher - Network Dev. Skills: TCP/IP, Socket Programming, TLS/SSL, OAuth2, Wireshark, Firewalls, DNS.",
        "role_title": "Network Infrastructure Architect"
    },
    {
        "id": 7,
        "domain": "Machine Learning & AI Engineering",
        "candidate_name": "George Clark (AI/ML Engineer)",
        "jd_text": "Role: Senior AI/ML Engineer. Skills Required: Python, PyTorch, TensorFlow, LLMs, Transformer Architecture, Deep Learning, MLOps, Model Fine-Tuning.",
        "resume_text": "George Clark - AI Researcher. Skills: Python, PyTorch, TensorFlow, Scikit-Learn, Deep Learning, LLMs, NLP, Computer Vision.",
        "role_title": "Senior AI/ML Engineer"
    },
    {
        "id": 8,
        "domain": "Cybersecurity & Web Security",
        "candidate_name": "Hannah Abbott (Security Lead)",
        "jd_text": "Role: Application Security Lead. Skills Required: Penetration Testing, OWASP Top 10, Cryptography, JWT, Threat Modeling, Static Code Analysis, Network Security.",
        "resume_text": "Hannah Abbott - Cyber Specialist. Skills: Penetration Testing, OWASP Top 10, Cryptography, JWT, Vulnerability Scanning, Security Auditing.",
        "role_title": "Application Security Lead"
    },
    {
        "id": 9,
        "domain": "DevOps & Cloud SRE",
        "candidate_name": "Ian Malcolm (Staff SRE)",
        "jd_text": "Role: Staff DevOps & SRE Lead. Skills Required: Docker, Kubernetes, AWS, Terraform, CI/CD Pipelines, Prometheus, Grafana, Infrastructure as Code.",
        "resume_text": "Ian Malcolm - SRE Engineer. Skills: Docker, Kubernetes, AWS, Terraform, CI/CD, Prometheus, Grafana, Linux Administration.",
        "role_title": "Staff DevOps & SRE Lead"
    },
    {
        "id": 10,
        "domain": "Software Architecture & Clean Code",
        "candidate_name": "Julia Roberts (Software Architect)",
        "jd_text": "Role: Lead Software Architect. Skills Required: Java, Design Patterns, SOLID Principles, TDD, Clean Architecture, Refactoring, Domain Driven Design.",
        "resume_text": "Julia Roberts - Architect. Skills: Java, Spring Boot, Design Patterns, SOLID Principles, Unit Testing, Clean Code, Microservices.",
        "role_title": "Lead Software Architect"
    }
]

def run_single_cse_case(cse_case: Dict[str, Any], previous_asked_questions: List[str]) -> Dict[str, Any]:
    resumes_dir = os.path.join("uploads", "resumes")
    os.makedirs(resumes_dir, exist_ok=True)
    sim_resume_path = os.path.join(resumes_dir, f"sim_resume_{cse_case['id']}.txt")
    with open(sim_resume_path, "w", encoding="utf-8") as f:
        f.write(cse_case["resume_text"])

    initial_state = {
        "user_id": 100 + cse_case["id"],
        "session_id": cse_case["id"],
        "candidate_name": cse_case["candidate_name"],
        "resume_path": sim_resume_path,
        "jd_text": cse_case["jd_text"],
        "previous_questions": list(previous_asked_questions),
        "user_answers": {}
    }

    start_time = time.time()
    state_after_questions = interview_graph.invoke(initial_state)

    questions = state_after_questions.get("questions", [])
    question_texts = [q.get("question_text", "") for q in questions]

    # Evaluate candidate answers for generated questions
    feedbacks = []
    sample_answers = [
        "I analyze system requirements, measure Big-O complexity, and use hash tables or balanced trees to optimize bottleneck routines.",
        "I design stateless microservices with distributed caching (Redis) and event-driven message queues (Kafka) to handle high concurrency.",
        "I write modular code with clear separation of concerns, comprehensive unit tests, and CI/CD automated validation pipelines.",
        "I evaluate database queries using EXPLAIN plans, construct targeted indexes, and apply connection pooling for high throughput.",
        "I handle thread synchronization using mutexes, minimize critical sections, and avoid deadlock conditions through resource ordering.",
        "I enforce TLS encryption, robust token validation (JWT), and rate-limiting middleware to protect endpoints."
    ]

    for idx, q_obj in enumerate(questions):
        q_text = q_obj.get("question_text", "Explain your technical approach.")
        ans_text = sample_answers[idx % len(sample_answers)]
        fb = feedback_agent.evaluate_answer(q_text, ans_text)
        feedbacks.append(fb)

    state_after_questions["question_feedbacks"] = feedbacks

    # Generate Final Report & PDF
    final_state = generate_report_node(state_after_questions)
    elapsed = round(time.time() - start_time, 2)

    return {
        "case_id": cse_case["id"],
        "domain": cse_case["domain"],
        "candidate_name": cse_case["candidate_name"],
        "role_title": final_state.get("role_title", cse_case["role_title"]),
        "ats_score": final_state.get("ats_score", 0.0),
        "match_percentage": final_state.get("match_percentage", 0.0),
        "matched_skills": final_state.get("matched_skills", []),
        "missing_skills": final_state.get("missing_skills", []),
        "questions_generated": question_texts,
        "num_questions": len(question_texts),
        "overall_score": final_state.get("overall_score", 0.0),
        "pdf_path": final_state.get("pdf_path", ""),
        "elapsed_seconds": elapsed,
        "is_completed": final_state.get("is_completed", False)
    }

def test_10_cse_pipeline_execution():
    print("\n========================================================")
    print("STARTING 10 CSE MULTI-AGENT PIPELINE TEST SUITE")
    print("========================================================\n")

    results = []
    all_asked_questions = []

    for cse in CSE_TEST_CASES:
        print(f"Executing Case #{cse['id']}: {cse['domain']}...")
        res = run_single_cse_case(cse, all_asked_questions)
        results.append(res)
        all_asked_questions.extend(res["questions_generated"])
        print(f" -> Completed in {res['elapsed_seconds']}s | Score: {res['overall_score']}% | PDF: {res['pdf_path']}")

    # Verification 1: All 10 cases completed successfully
    completed_count = sum(1 for r in results if r["is_completed"])
    assert completed_count == 10, f"Expected 10 completed cases, got {completed_count}"

    # Verification 2: Question Uniqueness Check across all 10 CSE cases
    question_set = set(q.lower().strip() for q in all_asked_questions)
    duplicate_count = len(all_asked_questions) - len(question_set)
    print(f"\nTotal Questions Generated Across 10 CSE Cases: {len(all_asked_questions)}")
    print(f"Unique Question Texts: {len(question_set)}")
    print(f"Duplicate Count: {duplicate_count}")

    assert duplicate_count == 0, f"Found {duplicate_count} repeated questions across the pipeline!"

    # Save detailed markdown report artifact
    report_md_path = os.path.join("uploads", "reports", "cse_10_pipeline_test_report.md")
    os.makedirs(os.path.dirname(report_md_path), exist_ok=True)

    report_content = f"""# 10 CSE Multi-Agent AI System Pipeline Test Report

**Execution Timestamp**: {time.strftime('%Y-%m-%d %H:%M:%S')}  
**Total Test Cases**: 10 CSE Domains  
**Completed Cases**: {completed_count} / 10  
**Total Questions Generated**: {len(all_asked_questions)}  
**Unique Questions**: {len(question_set)} (100% Unique - 0 Repetitions)  

---

## 1. Summary of 10 CSE Domains Tested

| # | CSE Domain | Candidate / Role | ATS Score | Match % | Overall Score | Elapsed (s) | PDF Report |
|---|------------|------------------|-----------|---------|---------------|-------------|------------|
"""
    for r in results:
        report_content += f"| {r['case_id']} | {r['domain']} | {r['role_title']} | {r['ats_score']}% | {r['match_percentage']}% | {r['overall_score']}% | {r['elapsed_seconds']}s | `{os.path.basename(r['pdf_path'])}` |\n"

    report_content += "\n---\n\n## 2. Question Deduplication & Uniqueness Audit\n\n"
    for r in results:
        report_content += f"### Case #{r['case_id']}: {r['domain']}\n"
        for i, q in enumerate(r['questions_generated'], 1):
            report_content += f"{i}. {q}\n"
        report_content += "\n"

    with open(report_md_path, "w", encoding="utf-8") as f:
        f.write(report_content)

    print(f"\nPipeline Test Report successfully generated at: {report_md_path}")
    print("========================================================\n")

if __name__ == "__main__":
    test_10_cse_pipeline_execution()
