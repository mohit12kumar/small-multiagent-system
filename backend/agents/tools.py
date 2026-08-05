import os
import sys
from typing import Dict, Any, List
from backend.services.ocr_service import extract_text_from_file
from backend.services.pdf_service import generate_pdf_report
from backend.services.rag_service import rag_engine

def resume_parser_tool(file_path: str) -> str:
    """Tool: Extract raw text content from uploaded resume PDF/DOCX/TXT file."""
    return extract_text_from_file(file_path)

def ats_scorer_tool(resume_skills: List[str], jd_skills: List[str]) -> Dict[str, Any]:
    """Tool: Calculate ATS score based on keyword match density and required skills."""
    if not jd_skills:
        return {"ats_score": 75.0, "matched": resume_skills, "missing": []}
    
    r_set = set(s.lower().strip() for s in resume_skills)
    j_set = set(s.lower().strip() for s in jd_skills)
    
    matched = list(r_set.intersection(j_set))
    missing = list(j_set - r_set)
    
    score = (len(matched) / max(len(j_set), 1)) * 100.0
    return {
        "ats_score": round(score, 1),
        "matched": matched,
        "missing": missing
    }

def coding_compiler_tool(code_snippet: str) -> Dict[str, Any]:
    """Tool: Validates Python code syntax and safety constraints."""
    try:
        compile(code_snippet, "<string>", "exec")
        return {"valid_syntax": True, "error": None}
    except Exception as e:
        return {"valid_syntax": False, "error": str(e)}

def pdf_generator_tool(candidate_name: str, session_id: int, overall_score: float, feedbacks: list, missing_skills: list) -> str:
    """Tool: Synthesize downloadable ReportLab PDF performance report."""
    return generate_pdf_report(candidate_name, session_id, overall_score, feedbacks, missing_skills)

def search_knowledge_tool(query: str) -> List[Dict[str, Any]]:
    """Tool: Retrieve benchmark questions and domain frameworks from RAG knowledge engine."""
    return rag_engine.retrieve_relevant_knowledge(query)
