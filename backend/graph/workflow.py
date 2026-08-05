from langgraph.graph import StateGraph, START, END
from backend.graph.state import InterviewState
from backend.graph.nodes import (
    supervisor_node,
    parse_resume_node,
    parse_jd_node,
    match_skills_node,
    generate_questions_node,
    evaluate_answers_node,
    generate_report_node
)
from backend.graph.router import route_next_step

def build_interview_workflow():
    workflow = StateGraph(InterviewState)
    
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("parse_resume", parse_resume_node)
    workflow.add_node("parse_jd", parse_jd_node)
    workflow.add_node("match_skills", match_skills_node)
    workflow.add_node("generate_questions", generate_questions_node)
    workflow.add_node("evaluate_answers", evaluate_answers_node)
    workflow.add_node("generate_report", generate_report_node)
    
    # Entry point goes to Supervisor Router
    workflow.add_edge(START, "supervisor")
    
    # Dynamic Router Conditional Edges
    workflow.add_conditional_edges(
        "supervisor",
        route_next_step,
        {
            "parse_resume": "parse_resume",
            "match_skills": "match_skills",
            "generate_questions": "generate_questions",
            "evaluate_answers": "evaluate_answers",
            "generate_report": "generate_report",
            "FINISH": END
        }
    )
    
    # Node Transitions
    workflow.add_edge("parse_resume", "parse_jd")
    workflow.add_edge("parse_jd", "match_skills")
    workflow.add_edge("match_skills", "generate_questions")
    workflow.add_edge("generate_questions", "supervisor")
    workflow.add_edge("evaluate_answers", "generate_report")
    workflow.add_edge("generate_report", END)
    
    return workflow.compile()

interview_graph = build_interview_workflow()
