from fastapi import FastAPI, BackgroundTasks, HTTPException
from src.models.schemas import WebhookPayload
from src.services.agent import GhostAgentSwarm
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ghost_developer")

app = FastAPI(title="Ghost Developer", description="Autonomous AI Developer Swarm")
swarm = GhostAgentSwarm()

@app.post("/webhook/github")
async def github_webhook(payload: WebhookPayload, background_tasks: BackgroundTasks):
    """
    Listens for GitHub issue events.
    If tagged/actioned, it kicks off the Ghost Agent in the background.
    """
    if payload.action not in ["opened", "reopened", "labeled"]:
        return {"message": "Ignored action"}
        
    logger.info(f"Received webhook for Issue #{payload.issue.number}")
    
    # Process asynchronously to avoid webhook timeouts
    background_tasks.add_task(swarm.solve_issue, payload.issue)
    
    return {
        "status": "accepted",
        "message": f"Ghost Developer dispatched for issue #{payload.issue.number}"
    }

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "ghost-developer"}
