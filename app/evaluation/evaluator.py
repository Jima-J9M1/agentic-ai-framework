from app.schemas import ToolStep
from app.tools.math_tools import  TOOLS
from app.evaluation.schemas import EvaluationResult

class AgentEvaluator:
    def evaluate(
        self,
        task: str,
        plan: list[ToolStep],
        results: list[dict],
        critic_approved: bool
    ) -> EvaluationResult:

        issues = []

        # 1. Plan validity
        valid_steps = 0
        for step in plan:
            if step.tool in TOOLS and "a" in step.args and "b" in step.args:
                valid_steps += 1
            else:
                issues.append(f"Invalid tool or args: {step}")

        plan_validity = valid_steps / max(len(plan), 1)

        # 2. Hallucination detection
        hallucinations = [
            step for step in plan if step.tool not in TOOLS
        ]
        hallucination_score = 1.0 - (len(hallucinations) / max(len(plan), 1))

        # 3. Critic accuracy
        critic_accuracy = 1.0
        if critic_approved and hallucinations:
            critic_accuracy = 0.0
            issues.append("Critic approved hallucinated plan")
        
        # 4. Memory consistency
        mismatches = 0
        for r in results:
            expected = TOOLS[r["tool"]](r["args"])
            if expected != r["result"]:
                mismatches += 1
                issues.append(f"Memory mismatch on {r}")

        memory_consistency = 1.0 - (mismatches / max(len(results), 1))

        return EvaluationResult(
            plan_validity=round(plan_validity, 2),
            hallucination_score=round(hallucination_score, 2),
            critic_accuracy=round(critic_accuracy, 2),
            memory_consistency=round(memory_consistency, 2),
            issues=issues
        )
