from app.memory.session_memory import SessionMemory
from app.memory.vector_store import VectorMemory
from app.schemas import ToolResult
from app.logging import logger
from pydantic import ValidationError
from app.tools.math_tools import TOOLS

memory_manager = SessionMemory()
class WorkerAgent:
    def __init__(self, memory_manager:SessionMemory):
        self.memory_manager = memory_manager

    def execute(self, steps:dict[str, int], session_id:str):
        session_memory = self.memory_manager.get(session_id)
        results = []
        for step in steps:
            tool = step.tool
            args = step.args
            result = TOOLS[tool](args)
            record = f"Tool: {tool} Args: {args} Result: {result}"
            session_memory.add_action(record)
            results.append({
                "tool":tool,
                "args":args,
                "result": result
            })

        session_memory.maybe_summarize()

        logger.info(f"Worker executed {len(steps)} steps: {results}")
        return results
