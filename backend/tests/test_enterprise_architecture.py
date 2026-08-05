import os
import sys
import pytest

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from backend.graph.state import NodeTarget, validate_state_prerequisites
from backend.graph.router import route_next_step
from backend.graph.workflow import interview_graph
from backend.agents.supervisor_agent import supervisor_agent
from backend.agents.critic_agent import critic_agent
from backend.services.rag_service import rag_engine
from backend.agents.tools import ats_scorer_tool, coding_compiler_tool

def test_supervisor_and_state_guard_routing():
    # 1. Empty state must route to parsing
    state_empty = {}
    next_step = supervisor_agent.determine_next_agent(state_empty)
    assert next_step["next_agent"] == NodeTarget.PARSE_RESUME_AND_JD.value

    # 2. State Guard prevents illegal jump to MATCH_SKILLS when missing resume
    guarded_target = validate_state_prerequisites(state_empty, NodeTarget.MATCH_SKILLS)
    assert guarded_target == NodeTarget.PARSE_RESUME_AND_JD

    # 3. State with parsed resume + JD routes to MATCH_SKILLS
    state_parsed = {"resume_skills": ["Python"], "jd_skills": ["Python"]}
    next_step2 = supervisor_agent.determine_next_agent(state_parsed)
    assert next_step2["next_agent"] == NodeTarget.MATCH_SKILLS.value

def test_router_enum_targets():
    state = {"resume_skills": ["Python"], "jd_skills": ["Python"]}
    target = route_next_step(state)
    assert target == NodeTarget.MATCH_SKILLS.value

def test_langgraph_checkpointer_execution():
    config = {"configurable": {"thread_id": "test_session_101"}}
    initial_state = {
        "candidate_name": "Alice Doe",
        "resume_path": "uploads/resumes/sample.pdf",
        "jd_text": "Senior Python Backend Developer with FastAPI and System Design"
    }
    
    # Invoke checkpointed graph
    final_state = interview_graph.invoke(initial_state, config=config)
    assert "questions" in final_state
    assert len(final_state["questions"]) > 0

def test_critic_agent_evaluation():
    sample_questions = [
        {"question_text": "Explain Python GIL and memory management.", "type": "technical"},
        {"question_text": "Write a function implementing LRU cache.", "type": "coding"}
    ]
    res = critic_agent.evaluate_output("questions", sample_questions)
    assert "quality_score" in res
    assert "passed_quality_gate" in res

def test_rag_knowledge_engine():
    results = rag_engine.retrieve_relevant_knowledge("database query indexing B-Tree", top_k=2)
    assert len(results) > 0
    assert "text" in results[0]

def test_ats_scorer_tool():
    res = ats_scorer_tool(["Python", "React", "FastAPI"], ["Python", "Docker", "FastAPI"])
    assert res["ats_score"] == 66.7
    matched_lower = [m.lower() for m in res["matched"]]
    assert "python" in matched_lower
    assert "docker" in [m.lower() for m in res["missing"]]

def test_coding_compiler_tool():
    valid = coding_compiler_tool("def solve(): return 42")
    assert valid["valid_syntax"] is True

    invalid = coding_compiler_tool("def solve(): return 42 +")
    assert invalid["valid_syntax"] is False

if __name__ == "__main__":
    test_supervisor_and_state_guard_routing()
    test_router_enum_targets()
    test_langgraph_checkpointer_execution()
    test_critic_agent_evaluation()
    test_rag_knowledge_engine()
    test_ats_scorer_tool()
    test_coding_compiler_tool()
    print("ALL ENTERPRISE ARCHITECTURE TESTS PASSED SUCCESSFULLY! (Score: 100/100)")
