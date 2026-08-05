import enum
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
    Standardized Pydantic envelope for all agent outputs.
    Guarantees confidence scoring, explainability reasoning, and review flags across the multi-agent system.
    """
    output: Dict[str, Any]
    confidence: float = Field(default=0.95, ge=0.0, le=1.0, description="Agent confidence score")
    reasoning: str = Field(..., description="Explainability reasoning for why output was generated")
    needs_review: bool = Field(default=False, description="Flag set to True if Critic quality score < 80%")
    agent_name: str = Field(..., description="Identifier of the executing agent")
