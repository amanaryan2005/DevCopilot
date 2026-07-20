from celery import Celery
from app.config import settings
from app.agents.graph import copilot_graph

celery_app = Celery(
    "copilot_tasks", 
    broker=settings.REDIS_URL, 
    backend=settings.REDIS_URL
)

@celery_app.task(name="tasks.process_pr_audit")
def process_pr_audit(repository: str, code_diff: str) -> str:
    initial_state = {
        "repository": repository,
        "code_diff": code_diff
    }
    
    # Run graph execution
    result = copilot_graph.invoke(initial_state)
    
    report = result.get("final_report", "Audit failed to produce output.")
    
    # Optional: Send payload back to GitHub PR API here
    print(f"\n================ AUDIT REPORT FOR {repository} ================\n")
    print(report)
    
    return report