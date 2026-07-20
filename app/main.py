from fastapi import FastAPI, HTTPException, status
from app.schemas.webhook import PullRequestPayload, AuditTaskResponse
from app.worker.celery_app import process_pr_audit

app = FastAPI(
    title="DevSecOps AI Copilot",
    version="1.0.0",
    description="Multi-Agent AI Code Review Engine"
)

@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "online", "service": "DevSecOps Copilot API"}

@app.post(
    "/api/v1/webhook/github", 
    response_model=AuditTaskResponse, 
    status_code=status.HTTP_202_ACCEPTED
)
async def handle_github_webhook(payload: PullRequestPayload):
    if not payload.code_diff.strip():
        raise HTTPException(
            status_code=400, 
            detail="Provided code diff cannot be empty."
        )

    # Queue background processing task
    task = process_pr_audit.delay(payload.repository, payload.code_diff)

    return AuditTaskResponse(
        status="queued",
        task_id=task.id,
        message=f"PR #{payload.pr_id} queued for multi-agent evaluation."
    )