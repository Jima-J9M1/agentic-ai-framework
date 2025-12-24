FORBIDDEN_KEYWORDS = [
    "medical", "diagnose", "treatment",
    "legal", "lawsuit",
    "password", "credit card"
]

class GuardAgent:
    def check(self, task:str):
        task = task.lower()
        for word in FORBIDDEN_KEYWORDS:
            if word in task:
                raise PermissionError("Task violates safety rules")
