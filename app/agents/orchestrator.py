
from app.agents.critic import CriticAgent
from app.agents.planner import PlannerAgent
from app.evaluation.llm_evaluator import LLMAgentEvaluator
from app.logging import logger
from app.evaluation.evaluator import AgentEvaluator


class AgentOrchestrator:
    def __init__(self, planner: PlannerAgent, critic: CriticAgent):
        self.planner = planner
        self.critic = critic
        self.evaluator = AgentEvaluator()
        self.llm_evaluator = LLMAgentEvaluator()


    def get_final_plan(self, task:str, session_id:str):
        plan = self.planner.plan(task, session_id)


        for _ in range(2):
            feedback = self.critic.review(task, plan)
            logger.info(f"Critic feedback: {feedback}")
            if feedback.approved:
                return plan, feedback.approved

            plan = self.planner.revise(task, feedback.suggestions or "Fix the issues")


        return plan , feedback.approved
        