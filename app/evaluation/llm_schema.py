from pydantic import BaseModel
from typing import List, Optional

class LLMEvaluationResult(BaseModel):
    intent_alignment: float
    reasoning_quality: float
    hallucination_risk: float
    overall_quality: float
    comments: Optional[List[str]] = []