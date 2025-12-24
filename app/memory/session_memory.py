

from app.logging import logger
from app.memory.summarizer import MemorySummarizer
from app.memory.vector_store import VectorMemory

class SessionMemory:
    def __init__(self):
        self.short_term = VectorMemory()
        self.long_term_summary = ""
        self.summarizer = MemorySummarizer()

    def add_action(self, text:str):
        self.short_term.add(text)

    def maybe_summarize(self):
      if len(self.short_term.texts) > 5:
        summary = self.summarizer.summarize(self.short_term.texts)
        logger.info(f"Summarized session memory: {summary}")
        self.long_term_summary = summary
        self.short_term.texts.clear()
        self.short_term.index.reset()
        self.short_term.timestamps.clear()


    def retrieve(self, query:str) -> SessionMemory:
        memory = self.short_term.search(query)
        
        if self.long_term_summary:
            memory.insert(0, f"Summary: {self.long_term_summary}")

        return memory


    

class SessionMemoryManger:
    def __init__(self):
        self.sessions: dict[str, SessionMemory] = {}

    def get(self, session_id:str) -> SessionMemory:
        if session_id not in self.sessions:
            self.sessions[session_id] = SessionMemory()
        return self.sessions[session_id]
    
   