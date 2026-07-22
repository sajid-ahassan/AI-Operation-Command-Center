from sqlalchemy import Column, Integer, String, DateTime,Boolean,ARRAY
from datetime import datetime
from uuid import uuid4
from app.database import Base

class Email(Base):
    __tablename__ = "emails"

    email_id = Column(String, primary_key=True, index=True)
    thread_id = Column(String, primary_key=True, index=True)
    sender = Column(String, index=True)
    subject = Column(String, index=True)
    body = Column(String)
    status = Column(String, default="received")
    timestamp = Column(DateTime, default=datetime.isoformat(datetime.utcnow()))
    

    category = Column(String, default="")
    priority = Column(String, default="")
    action = Column(ARRAY(String), default=[])
    confidence = Column(String, default="")
    requires_human_intervention = Column(Boolean, default=False)
    reason = Column(String, default="")
    
    
class Aproval(Base):
    __tablename__ = "approvals"

    id = Column(String, primary_key=True, index=True,default=lambda: str(uuid4()))
    email_id = Column(String, index=True)
    thread_id = Column(String, index=True)
    sender = Column(String, index=True)
    body = Column(String, default="")
    category = Column(String, default="")
    priority = Column(String, default="")
    action = Column(ARRAY(String), default=[])
    reason = Column(String, default="")
    approval_status = Column(String, default="pending")
    decision_by = Column(String, default="")
    decision_reason = Column(String, default="")
    timestamp = Column(DateTime, default=datetime.isoformat(datetime.utcnow()))