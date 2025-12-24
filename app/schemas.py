from pydantic import BaseModel
from typing import Dict, List, Optional

from app.evaluation.llm_schema import LLMEvaluationResult
from app.evaluation.schemas import EvaluationResult

class TaskRequest(BaseModel):
    session_id: str
    text:str

class ToolStep(BaseModel):
    tool:str
    args: Dict[str, int]


class ToolResult(BaseModel):
    tool:str
    args:Dict[str, int]
    result:int

class AgentResponse(BaseModel):
    result: List[ToolResult]
    evaluation: Dict[str, EvaluationResult | LLMEvaluationResult]
    
class CriticFeedback(BaseModel):
    approved: bool
    issues: Optional[List[str]] = None
    suggestions: Optional[List[str]] = None