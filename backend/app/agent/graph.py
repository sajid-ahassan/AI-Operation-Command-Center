from langgraph.graph import StateGraph,START, END

from psycopg_pool import ConnectionPool
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.types import interrupt

from langchain_openai import ChatOpenAI

from app.agent.models import email_decision
from app.agent.prompts import analysis_prompt

import requests
from typing import Literal

from dotenv import load_dotenv
import os
load_dotenv()

model = ChatOpenAI(model_name="gpt-5.4-nano", temperature=0.5, openai_api_key=os.getenv("OPENAI_API_KEY"))

DB_URL = os.getenv("DATABASE_URL")


class EmailState(StateGraph):
    email_id :str
    email_thread_id :str
    sender :str
    subject :str
    body :str
    
    category :str
    priority :str
    action :Literal['CREATE_CRM_LEAD', 'CREATE_SUPPORT_TICKET', 'CREATE_PROJECT', 'SCHEDULE_MEETING','SEND_QUOTATION']
    confidence :float
    requires_human_intervention :bool
    reason: str
    approval : dict
    
    
    
    
def analyse_email(state: EmailState):
    
    chain =  analysis_prompt | model.with_structured_output(email_decision)
    resp = chain.invoke({"subject": state['subject'], "body": state['body']})
    return {"category": resp.category, "priority": resp.priority, "action": resp.action, "requires_human_intervention": resp.requires_human_intervention, "confidence": resp.confidence, "reason": resp.reason}


def human_approval(state: EmailState):
    
    decision = interrupt(
        {
        'message':"waiting for human approval",
        'email_id':state['email_id'],
        "action":state['action']
    })
    
    return {'approval':decision}


def execute_action(state: EmailState):
 
    WEBHOOK_URL = 'https://vendor-such-fiction.ngrok-free.dev/webhook/9b7f42de-3f60-44cc-b59b-e55579cecd37'

    response = requests.post(WEBHOOK_URL, json=state)
    
    return state



# Decision section


def action_decision(state: EmailState) -> Literal["human_approval", "execute_action"]:
    if state['requires_human_intervention']:
        return "human_approval"
    else:
        return "execute_action"
    
    
connection_pool = ConnectionPool(conninfo=DB_URL)
checkpointer = PostgresSaver(connection_pool)

def build_graph():
    graph = StateGraph(EmailState) 

    graph.add_node("analyse_email",analyse_email)
    graph.add_node("human_approval",human_approval)
    graph.add_node("execute_action",execute_action)

    graph.add_edge(START, "analyse_email")
    graph.add_conditional_edges("analyse_email", action_decision)
    graph.add_edge("human_approval", 'execute_action')
    graph.add_edge("execute_action", END)

    workflow = graph.compile(checkpointer=checkpointer)
    return workflow




# inp = {"email_id": "12345", "sender": 'sajid', "subject": 'cancel yearly subscription', "body": 'I am facing problem so I want to cancel my subscription', "category": '', "priority": '', "action": '', "requires_human_intervention": False}

# result = build_graph().invoke(inp)
# print(result)
