import json
from app.llm.client import LLMClient
from app.logging import logger
from app.schemas import CriticFeedback, ToolStep


class CriticAgent:
    def __init__(self):
        self.llm = LLMClient()

    def build_prompt(self, task:str,plan:list[ToolStep]) -> str:
        return f"""

        You are a critic agent.

        User task:
        {task}

        Proposed plan:
        {[step.model_dump_json() for step in plan]}

        Your Job:
         - Check the correctness
         - Check the missing steps
        - Check wrong tool usage


        Respond ONLY in JSON.

        Format:
        {{
            "approved": true | false,
            "issues": ['strings'],
            "suggestions": ["strings"]
        }}

        """

    def review(self, task:str, plan:list[ToolStep]) -> CriticFeedback:
        raw = self.llm.generate(self.build_prompt(task, plan))

        return CriticFeedback(**json.loads(raw))