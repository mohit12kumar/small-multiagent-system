from langgraph.graph import StateGraph, START, END
from backend.graph.state import InterviewState
from backend.graph.nodes import (
    parse_resume_node,
    parse_jd_node,
    match_skills_node,
    generate_questions_node,
    generate_report_node
)

def build_interview_workflow():
    workflow = StateGraph(InterviewState)
    
    workflow.add_node("parse_resume", parse_resume_node)
    workflow.add_node("parse_jd", parse_jd_node)
    workflow.add_node("match_skills", match_skills_node)
    workflow.add_node("generate_questions", generate_questions_node)
    workflow.add_node("generate_report", generate_report_node)
    
    workflow.add_edge(START, "parse_resume")
    workflow.add_edge("parse_resume", "parse_jd")
    workflow.add_edge("parse_jd", "match_skills")
    workflow.add_edge("match_skills", "generate_questions")
    workflow.add_edge("generate_questions", END)
    
    return workflow.compile()

interview_graph = build_interview_workflow()
