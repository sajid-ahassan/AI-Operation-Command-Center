from pydantic import BaseModel,EmailStr

class EmailRequest(BaseModel):
    sender: EmailStr
    header: str
    body: str