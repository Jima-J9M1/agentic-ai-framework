from pydantic import BaseModel
from typing import List, Optional

class EvaluationResult(BaseModel):
    plan_validity: float
    hallucination_score: float
    critic_accuracy: float
    memory_consistency: float
    issues: Optional[List[str]] = []
