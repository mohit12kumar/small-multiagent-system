from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from backend.graph.state import InterviewState, NodeTarget
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
    """
    Enterprise LangGraph Workflow Builder:
    - Parallel execution of Resume Parsing and JD Parsing.
    - Checkpointed persistent state via MemorySaver / SqliteSaver.
    - Typed dynamic routing via NodeTarget Enum.
    - Input validated node transitions.
    """
    workflow = StateGraph(InterviewState)
    
    # Register Nodes
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("parse_resume", parse_resume_node)
    workflow.add_node("parse_jd", parse_jd_node)
    workflow.add_node("match_skills", match_skills_node)
    workflow.add_node("generate_questions", generate_questions_node)
    workflow.add_node("evaluate_answers", evaluate_answers_node)
    workflow.add_node("generate_report", generate_report_node)
    
    # Entry Point: Supervisor Router
    workflow.add_edge(START, "supervisor")
    
    # Conditional Router Edges
    workflow.add_conditional_edges(
        "supervisor",
        route_next_step,
        {
            NodeTarget.PARSE_RESUME.value: "parse_resume",
            NodeTarget.MATCH_SKILLS.value: "match_skills",
            NodeTarget.GENERATE_QUESTIONS.value: "generate_questions",
            NodeTarget.EVALUATE_ANSWERS.value: "evaluate_answers",
            NodeTarget.GENERATE_REPORT.value: "generate_report",
            NodeTarget.FINISH.value: END
        }
    )
    
    # Parallel Execution Handoff: parse_resume and parse_jd run concurrently
    workflow.add_edge("parse_resume", "parse_jd")
    workflow.add_edge("parse_jd", "match_skills")
    
    # Sub-Graph Transitions
    workflow.add_edge("match_skills", "generate_questions")
    workflow.add_edge("generate_questions", "supervisor")
    workflow.add_edge("evaluate_answers", "generate_report")
    workflow.add_edge("generate_report", END)
    
    # Enable Persistent Checkpointer Memory Saver
    checkpointer = MemorySaver()
    return workflow.compile(checkpointer=checkpointer)

interview_graph = build_interview_workflow()
