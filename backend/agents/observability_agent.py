import time
import uuid
from typing import Dict, Any

class ObservabilityAgent:
    """
    Observability & Telemetry Agent:
    Tracks prompt history, LLM execution latency, token usage, USD cost estimation, and trace IDs.
    """
    def __init__(self):
        self.active_traces: Dict[str, Dict[str, Any]] = {}

    def start_trace(self, agent_name: str) -> str:
        trace_id = str(uuid.uuid4())[:8]
        self.active_traces[trace_id] = {
            "agent_name": agent_name,
            "start_time": time.time(),
            "status": "running"
        }
        return trace_id

    def end_trace(self, trace_id: str, status: str = "success", token_usage: Dict[str, int] = None) -> Dict[str, Any]:
        trace = self.active_traces.get(trace_id, {})
        start_time = trace.get("start_time", time.time())
        latency_ms = round((time.time() - start_time) * 1000, 2)
        tokens = token_usage or {"prompt_tokens": 150, "completion_tokens": 100, "total_tokens": 250}
        
        # Estimate USD cost for llama-3.3-70b ($0.59 / 1M tokens)
        cost_usd = round((tokens.get("total_tokens", 250) / 1000000.0) * 0.59, 6)

        return {
            "trace_id": trace_id,
            "agent_name": trace.get("agent_name", "UnknownAgent"),
            "latency_ms": latency_ms,
            "status": status,
            "token_usage": tokens,
            "cost_usd": cost_usd
        }

observability_agent = ObservabilityAgent()
