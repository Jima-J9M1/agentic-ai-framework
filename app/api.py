from fastapi import APIRouter, HTTPException

from app.agents.critic import CriticAgent
from app.agents.guard import GuardAgent
from app.agents.orchestrator import AgentOrchestrator
from app.agents.planner import PlannerAgent
from app.agents.worker import WorkerAgent
from app.logging import logger
from app.memory.session_memory import SessionMemory, SessionMemoryManger
from app.schemas import AgentResponse, TaskRequest

router = APIRouter()
memory_manager = SessionMemoryManger()
guard  = GuardAgent()
planner = PlannerAgent(memory_manager)
worker = WorkerAgent(memory_manager)
critic = CriticAgent()
orchestrator = AgentOrchestrator(planner, critic)


@router.post("/agent", response_model= AgentResponse)
def run_agent(req: TaskRequest):
    logger.info(f"New task received: {req.text}")
    try:
        guard.check(req.text)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

    plan, approved = orchestrator.get_final_plan(req.text, req.session_id)
    logger.info(f"Planner generated {len(plan)} steps")

    if not plan:
        raise HTTPException(status_code=400, detail="No steps generated")
    
    results = worker.execute(plan, req.session_id)

    deterministic_eval = orchestrator.evaluator.evaluate(
        task = req.text,
        plan = plan,
        results = results,
        critic_approved = approved,
    )

    session_memory = memory_manager.get(req.session_id)
    retreived_memory = session_memory.retrieve(req.text)

    llm_eval = orchestrator.llm_evaluator.evaluate(
        task = req.text,
        plan=plan,
        results=results,
        memory=retreived_memory,
        critic_approved=approved,
    )

    logger.info(f"Results: {results}")
    logger.info(f"Evaluation: {deterministic_eval.model_dump()}")
    print(
        ">>>> evaluation: ", deterministic_eval.model_dump(), llm_eval.model_dump()
    )
    return {
        "result": results,
        "evaluation": {
            "deterministic":deterministic_eval.model_dump(),
            "llm_based":llm_eval.model_dump(),
        }
    }

    