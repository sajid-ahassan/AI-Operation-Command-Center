from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from app.database import get_db
from sqlalchemy.orm import Session
from app.models import Email
router = APIRouter()

from app.agent.graph import build_graph
from app.services.initiate_aproval import add_aproval_request
workflow = build_graph()



@router.post("/api/process_email/{email_id}")
def process_email(email_id: str, db: Annotated[Session, Depends(get_db)]):
    
    email = db.query(Email).filter(Email.email_id == email_id).first()
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    
    config={
        "configurable":{
            "thread_id": f"email_{email.email_id}"
        }
    }
    
    res = workflow.invoke({
        "email_id": email.email_id,
        "email_thread_id": email.thread_id,
        "sender": email.sender,
        "subject": email.subject,
        "body": email.body,
        "category": "",
        "priority": "",
        "action":"",
        "requires_human_intervention": False,
        "confidence": 0.0,
        "reason": ""
    },config=config)
    
    email.category = res['category']
    email.priority = res['priority']
    email.action = res['action']
    email.requires_human_intervention = res['requires_human_intervention']
    email.confidence = res['confidence']
    email.reason = res['reason']
    email.status = "action_executed"
    email.reason = res['reason'] 
    
    if "__interrupt__" in res:

        email.status = "awaiting_human_approval"
        payload = {
            "body": res['body'],
            "category": res['category'],
            "priority": res['priority'],
            "action": res['action'],
            "reason": res['reason'],
        }

        add_aproval_request(
            email_id=email.email_id,
            thread_id=email.thread_id,
            sender=email.sender,
            db=db,
            payload=payload
        )

        db.commit()

        return {
            "message": "Waiting for human approval, interupted request",
            "email_id": email.email_id,
            "thread_id": email.thread_id,
            "sender": email.sender,
            "status": email.status
        }
    
    
    
    db.commit()
    
    return {"message": "Email execution successfull", "email_id": email.email_id,"thread_id": email.thread_id,"sender": email.sender,"status": email.status}