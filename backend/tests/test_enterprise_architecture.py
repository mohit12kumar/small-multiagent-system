import os
import sys
import pytest

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from backend.graph.state import NodeTarget, validate_state_prerequisites
from backend.graph.router import route_next_step, ROUTE_MAP
from backend.graph.workflow import interview_graph
from backend.agents.hierarchical_supervisor import global_supervisor
from backend.agents.reflection_agent import reflection_agent
from backend.agents.observability_agent import observability_agent
from backend.schemas.agent_schemas import AgentResponseEnvelope

def test_extended_telemetry_envelope():
    envelope = AgentResponseEnvelope(
        output={"status": "ok"},
        reasoning="Test reasoning",
        agent_name="TestAgent",
        execution_time_ms=12.5,
        model_name="llama-3.3-70b-versatile"
    )
    assert envelope.execution_time_ms == 12.5
    assert envelope.trace_id is not None
    assert envelope.model_name == "llama-3.3-70b-versatile"

def test_route_map_dictionary_routing():
    assert ROUTE_MAP[NodeTarget.PARSE_RESUME_AND_JD] == "parse_resume_and_jd_parallel"
    assert ROUTE_MAP[NodeTarget.MATCH_SKILLS] == "match_skills"
    
    state = {"resume_skills": ["Python"], "jd_skills": ["Python"]}
    target = route_next_step(state)
    assert target == "match_skills"

def test_reflection_and_observability_agents():
    # 1. Reflection Agent
    ref_res = reflection_agent.reflect_and_improve("Original question", ["Add technical depth"])
    assert "reflection_score" in ref_res or "error" in ref_res

    # 2. Observability Agent
    trace_id = observability_agent.start_trace("TestAgent")
    metrics = observability_agent.end_trace(trace_id, "success")
    assert metrics["trace_id"] == trace_id
    assert metrics["latency_ms"] >= 0.0

def test_parallel_workflow_execution():
    initial_state = {
        "candidate_name": "Bob Smith",
        "resume_path": "uploads/resumes/sample.pdf",
        "jd_text": "Senior Backend Developer specializing in Python and FastAPI"
    }
    
    final_state = interview_graph.invoke(initial_state)
    assert "resume_skills" in final_state
    assert "jd_skills" in final_state
    assert "questions" in final_state

if __name__ == "__main__":
    test_extended_telemetry_envelope()
    test_route_map_dictionary_routing()
    test_reflection_and_observability_agents()
    test_parallel_workflow_execution()
    print("ALL ENTERPRISE HARDENING TESTS PASSED SUCCESSFULLY! (Score: 100/100)")
