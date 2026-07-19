
from pydantic import BaseModel,Field
from typing import List, Dict, Any, Annotated, Optional

class email_decision(BaseModel):
    
    category :str = Field(..., description="Category of the email")
    priority :str = Field(..., description="Priority of the email")
    action :str = Field(..., description="Action to be taken for the email")
    confidence :float = Field(..., description="Confidence level of the decision")
    requires_human_intervention :bool = Field(..., description="Whether the email requires human intervention")
    reason :str = Field(..., description="Reason for the decision")