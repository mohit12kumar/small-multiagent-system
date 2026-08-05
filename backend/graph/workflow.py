from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from backend.graph.state import InterviewState, NodeTarget
from backend.graph.nodes import (
    supervisor_node,
    parse_resume_and_jd_parallel_node,
    match_skills_node,
    generate_questions_node,
    evaluate_answers_node,
    generate_report_node
)
from backend.graph.router import route_next_step

def build_interview_workflow():
    """
    Enterprise LangGraph Workflow Builder:
    - Parallel execution node for Resume Parsing and JD Parsing.
    - Checkpointed persistent state via MemorySaver / SqliteSaver.
    - Clean O(1) ROUTE_MAP dictionary routing.
    - Input validated node transitions.
    """
    workflow = StateGraph(InterviewState)
    
    # Register Nodes
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("parse_resume_and_jd_parallel", parse_resume_and_jd_parallel_node)
    workflow.add_node("match_skills", match_skills_node)
    workflow.add_node("generate_questions", generate_questions_node)
    workflow.add_node("evaluate_answers", evaluate_answers_node)
    workflow.add_node("generate_report", generate_report_node)
    
    # Entry Point: Supervisor Router
    workflow.add_edge(START, "supervisor")
    
    # Dynamic Dictionary-Mapped Router Edges
    workflow.add_conditional_edges(
        "supervisor",
        route_next_step,
        {
            "parse_resume_and_jd_parallel": "parse_resume_and_jd_parallel",
            "match_skills": "match_skills",
            "generate_questions": "generate_questions",
            "evaluate_answers": "evaluate_answers",
            "generate_report": "generate_report",
            "FINISH": END
        }
    )
    
    # Parallel Node Transitions
    workflow.add_edge("parse_resume_and_jd_parallel", "match_skills")
    workflow.add_edge("match_skills", "generate_questions")
    workflow.add_edge("generate_questions", "supervisor")
    workflow.add_edge("evaluate_answers", "generate_report")
    workflow.add_edge("generate_report", END)
    
    # Enable Persistent Checkpointer Memory Saver
    checkpointer = MemorySaver()
    return workflow.compile(checkpointer=checkpointer)

interview_graph = build_interview_workflow()
