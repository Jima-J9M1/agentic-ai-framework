from collections import deque

SESSION_MEMORY = {}

def get_session(session_id:str):
    if session_id not in SESSION_MEMORY:
        SESSION_MEMORY[session_id] = deque(maxlen=10)
    return SESSION_MEMORY[session_id]
