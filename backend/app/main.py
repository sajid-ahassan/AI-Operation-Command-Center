from fastapi import FastAPI

from app.routers import email, aproval,agent 
app = FastAPI()

## ui part start

from fastapi.middleware.cors import CORSMiddleware


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

## ui part end

app.include_router(email.router)
app.include_router(aproval.router)
app.include_router(agent.router)

from app.database import engine, Base
from app.models import Email, Aproval

Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}


