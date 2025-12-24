import json
import re
from app.llm.client import LLMClient
from app.evaluation.llm_schema import LLMEvaluationResult
from app.schemas import ToolStep

class LLMAgentEvaluator:
    def __init__(self):
        self.llm = LLMClient()

    def build_prompt(
        self,
        task: str,
        plan: list[ToolStep],
        results: list[dict],
        memory: list[str],
        critic_approved: bool
    ) -> str:
        return f"""
You are an evaluation agent.

Evaluate the agent behavior for correctness and quality.

User task:
{task}

Plan:
{[step.model_dump() for step in plan]}

Execution results:
{results}

Retrieved memory:
{memory}

Critic approved:
{critic_approved}

Score each category from 0.0 to 1.0.

Return ONLY valid JSON:

{{
  "intent_alignment": number,
  "reasoning_quality": number,
  "hallucination_risk": number,
  "overall_quality": number,
  "comments": ["string"]
}}
"""

    def evaluate(
        self,
        task: str,
        plan: list[ToolStep],
        results: list[dict],
        memory: list[str],
        critic_approved: bool
    ) -> LLMEvaluationResult:

        raw = self.llm.generate(
            self.build_prompt(task, plan, results, memory, critic_approved)
        )

        # Try direct parsing first, then extract with regex if needed
        try:
            parsed = json.loads(raw.strip())
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", raw, re.DOTALL)
            if not match:
                raise ValueError(f"Failed to find JSON in LLM output: {raw}")
            parsed = json.loads(match.group(0))
        
        print(">>>> parsed: ", parsed)
        return LLMEvaluationResult(**parsed)

