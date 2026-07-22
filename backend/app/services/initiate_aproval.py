from sqlalchemy.orm import Session
from app.models import Aproval

def add_aproval_request(email_id: str, db: Session,payload: dict):
    approval_request = Aproval(email_id=email_id)
    approval_request.thread_id = payload.get("thread_id", "")
    approval_request.body = payload.get("body", "")
    approval_request.sender = payload.get("sender", "")
    approval_request.category = payload.get("category", "")
    approval_request.priority = payload.get("priority", "")
    approval_request.action = payload.get("action", "")
    approval_request.reason = payload.get("reason", "")
    db.add(approval_request)
    db.commit()
    db.refresh(approval_request)
    return approval_request