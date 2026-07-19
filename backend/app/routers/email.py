from fastapi import APIRouter,Depends,HTTPException,BackgroundTasks
from typing import Annotated


from app.database import get_db
from sqlalchemy.orm import Session

from app.schemas import EmailRequest
from app.models import Email

from app.agent.graph import build_graph

router = APIRouter()
workflow = build_graph()

@router.post("/api/webhook")
def webhook_endpoint(payload: EmailRequest, db: Annotated[Session, Depends(get_db)]):
    
    data = Email(
        sender=payload.sender,
        subject=payload.header,
        body=payload.body,
        )

    db.add(data)
    db.commit() 
    db.refresh(data)
    return {
        "message": "Webhook received successfully",
        "email_id": data.id,
    }
    



    
