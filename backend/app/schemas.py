from pydantic import BaseModel,EmailStr

class EmailRequest(BaseModel):
    email_id : str
    thread_id : str
    sender: EmailStr
    header: str
    body: str