
from app.llm.client import LLMClient


class MemorySummarizer:
    def __init__(self):
        self.llm = LLMClient()

    def summarize(self, records:list[str]) -> str:
        prompt = f"""
        Summarize the following agent actions into stable, reusable knowledge.
        Remove numbers unless it is important.
        Be concise.

        Records:
        {chr(10).join(records)}
        
        Summary:
        """


        return self.llm.generate(prompt).strip()
