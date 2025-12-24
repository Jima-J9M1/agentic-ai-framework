import json
import re
from app.llm.client import LLMClient
from app.logging import logger
from app.memory.session_memory import SessionMemoryManger
from app.schemas import ToolStep

class PlannerAgent:
    def __init__(self, memory_manager:SessionMemoryManger):
        self.memory_manager = memory_manager
        self.llm = LLMClient()

    def build_prompt(self, task:str, memory:list[str])->str:
        memory = "\n".join(memory) if memory else None
        return f"""
        You are a Plannig agent.
        
        Relevant Past Context:
        {memory}
        You job:
        - Convert the user tasks in tool step
        - Use ONLY the allowed tools

        Allowed tools:
        - add(a, b)
        - subtract(a, b)
        - multiply(a, b)


        Rules:
        - Return ONLY valid JSON
        - No explanation
        - No markdown

        JSON format:
        [
        {{
            "tool": "add" | "subtract" | "multiply",
            "args": {{ "a":number, "b":number }}
        }}
        ]

        User task:
        {task}
        
        """
    def plan(self, task: str, session_id:str):
        memory_store = self.memory_manager.get(session_id) 
        memory = memory_store.retrieve(task)
        logger.info(f"Found {memory} relevant past context")
        prompt = self.build_prompt(task, memory)

        for attempt in range(3):
            raw = self.llm.generate(prompt)
            try:
                parsed = json.loads(raw)
                steps = [ToolStep(**step) for step in parsed]
                return steps
            except Exception:
                # retry on bad input
                continue

        raise ValueError("Failed to generate valid plan")


    def revise_prompt(self, task:str, feedback:str) -> str:
        return f"""
        You are revising your previous plan based on the feedback.


        User task:
        {task}

        Feedback:
        {feedback}

        Return a corrected plan.
        Use ONLY valid JSON (same format as before).
        """


    def revise(self, task:str, feedback:str) -> list[ToolStep]:
        prompt = self.revise_prompt(task, feedback)

        for _ in range(2):
            raw = self.llm.generate(prompt)
            try:
                return [ToolStep(**step) for step in json.loads(raw)]
            except Exception:
                continue


        raise ValueError("Failed to generate valid plan")

