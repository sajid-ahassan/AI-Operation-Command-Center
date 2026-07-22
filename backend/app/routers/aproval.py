from fastapi import APIRouter,Depends,HTTPException,BackgroundTasks
from typing import Annotated
from app.database import get_db
from sqlalchemy.orm import Session
from app.models import Aproval

from langgraph.types import Command

from app.agent.graph import build_graph
workflow = build_graph()

router = APIRouter()

@router.get("/api/panding_approval")
def get_panding_approval(db: Annotated[Session, Depends(get_db)]):
    approvals = db.query(Aproval).filter(Aproval.approval_status == "pending").all()
    
    if not approvals:
        #return empty list if no pending approvals found
        return []
    
    return approvals


@router.post("/api/approve/{approval_id}")
def approve_request(approval_id: str, db: Annotated[Session, Depends(get_db)],payload: dict):
    approval_request = db.query(Aproval).filter(Aproval.id == approval_id).first()
    
    if not approval_request:
        raise HTTPException(status_code=404, detail="Approval request not found")
    
    config = {"configurable": {"thread_id": f"email_{approval_request.email_id}"}}
    
    human_decision = {
        "approval": "approved",
        "action": payload.get("action", approval_request.action),
        "priority": payload.get("priority", approval_request.priority),
        "note": payload.get("note", "")
    }

    res = workflow.invoke(
        Command(resume={'approval': human_decision})
        ,config=config
    )
        
    approval_request.action = human_decision["action"]
    approval_request.priority = human_decision["priority"]
    approval_request.approval_status = "approved"
    approval_request.decision_by = "admin" 
    approval_request.decision_reason = "Task needed human intervention"
    db.commit()
    db.refresh(approval_request)
    
    return {"message": "Approval request approved successfully", "approval_id": approval_request.id, "result": res}


@router.post("/api/reject/{approval_id}")
def reject_request(approval_id: str, db: Annotated[Session, Depends(get_db)],payload: dict):
    approval_request = db.query(Aproval).filter(Aproval.id == approval_id).first()
    
    if not approval_request:
        raise HTTPException(status_code=404, detail="Approval request not found")
    
    
    config = {"configurable": {"thread_id": f"email_{approval_request.email_id}"}}
    human_decision = {
        "approval": "rejected",
        "action": payload.get("action", approval_request.action),
        "priority": payload.get("priority", approval_request.priority),
        "note": payload.get("note", "")
    }

    res = workflow.invoke(
        Command(resume={'approval': human_decision})
        ,config=config
    )
        
    
    approval_request.approval_status = "rejected"
    approval_request.decision_by = "admin" 
    approval_request.decision_reason = "Does not require human intervention"
    db.commit()
    db.refresh(approval_request)
    
    return {"message": "Approval request rejected successfully", "approval_id": approval_request.id,"result": res}