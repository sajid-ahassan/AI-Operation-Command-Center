from fastapi import FastAPI

from app.routers import email, aproval,agent 
app = FastAPI()
app.include_router(email.router)
app.include_router(aproval.router)
app.include_router(agent.router)

from app.database import engine, Base
from app.models import Email, Aproval

Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}


