from typing import Dict, Any, List
from backend.services.pdf_service import generate_pdf_report

class ReportGeneratorAgent:
    """
    Agent 8: Report Generator Agent
    Responsibilities:
    - Aggregate interview session scores across all answers
    - Calculate composite overall readiness score
    - Generate PDF report file & preparation roadmap
    """
    def generate_report(
        self,
        candidate_name: str,
        session_id: int,
        feedbacks: List[Dict[str, Any]],
        missing_skills: List[str]
    ) -> Dict[str, Any]:
        if not feedbacks:
            overall_score = 0.0
        else:
            overall_score = sum(f.get("overall_score", 0.0) for f in feedbacks) / len(feedbacks)
            
        pdf_path = generate_pdf_report(
            candidate_name=candidate_name,
            session_id=session_id,
            overall_score=overall_score,
            feedbacks=feedbacks,
            missing_skills=missing_skills
        )
        
        roadmap = [f"Master {skill} through hands-on practice projects." for skill in missing_skills[:4]]
        if not roadmap:
            roadmap = ["Review advanced system design patterns and concurrency models."]
            
        return {
            "overall_score": round(overall_score, 1),
            "pdf_path": pdf_path,
            "skill_gap_summary": {"missing_skills": missing_skills},
            "improvement_plan": {"roadmap_steps": roadmap}
        }

report_generator_agent = ReportGeneratorAgent()
