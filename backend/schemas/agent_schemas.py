import enum
import uuid
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class CompanyMode(str, enum.Enum):
    GENERAL = "general"
    AMAZON = "amazon"
    GOOGLE = "google"
    MICROSOFT = "microsoft"
    META = "meta"
    ADOBE = "adobe"

class AgentResponseEnvelope(BaseModel):
    """
    Enterprise Pydantic Agent Response Envelope:
    Guarantees confidence scoring, explainability reasoning, execution time, token metrics, trace ID, and review flags.
    """
    output: Dict[str, Any]
    confidence: float = Field(default=0.95, ge=0.0, le=1.0, description="Agent confidence score")
    reasoning: str = Field(..., description="Explainability reasoning for why output was generated")
    needs_review: bool = Field(default=False, description="Flag set to True if Critic quality score < 80%")
    agent_name: str = Field(..., description="Identifier of the executing agent")
    
    # Telemetry & Observability Fields
    success: bool = Field(default=True, description="Execution success flag")
    execution_time_ms: float = Field(default=0.0, description="Agent execution latency in milliseconds")
    token_usage: Dict[str, int] = Field(default_factory=lambda: {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0})
    model_name: str = Field(default="llama-3.3-70b-versatile", description="Executing LLM model identifier")
    trace_id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8], description="Unique execution trace ID")
    warnings: List[str] = Field(default_factory=list, description="Execution warning messages")
