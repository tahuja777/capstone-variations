# capstone/app/graph.py
from dotenv import load_dotenv
load_dotenv()  # load .env file

from typing import List, Literal, Optional
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langchain_core.tools import tool
import requests
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate

# --- Agent State with extracted query params ---
class QueryParameters(BaseModel):
    invoice_id: Optional[str] = None
    account_id: Optional[str] = None
    ticket_id: Optional[str] = None
    period: Optional[str] = None

class AgentState(BaseModel):
    history: List[str] = []
    intent: Literal["FAQ", "DataLookup", "Escalation"] | None = None
    query: str = ""
    query_params: Optional[QueryParameters] = None
    answer: Optional[str] = None
    evidence: List[str] = []
    errors: List[str] = []

MCP_SERVER_URL = "http://localhost:8000"

@tool
def account_lookup(account_id: str = None, company: str = None) -> dict:
    """
    Calls MCP server to look up account information by account_id or company.
    Returns account details and source reference.
    """
    payload = {"account_id": account_id, "company": company}
    r = requests.post(f"{MCP_SERVER_URL}/account_lookup", json=payload)
    r.raise_for_status()
    return r.json()

@tool
def invoice_status(account_id: str, period: str = None, invoice_id: str = None) -> dict:
    """
    Calls MCP server to get status info of invoice specified by invoice_id and account_id.
    """
    payload = {"account_id": account_id, "period": period, "invoice_id": invoice_id}
    r = requests.post(f"{MCP_SERVER_URL}/invoice_status", json=payload)
    r.raise_for_status()
    return r.json()

@tool
def ticket_summary(ticket_id: str, window_days: int = 90) -> dict:
    """
    Calls MCP server for a summary of support tickets for the given ticket_id.
    """
    payload = {"ticket_id": ticket_id, "window_days": window_days}
    print("ticket summary called payload", payload)
    r = requests.post(f"{MCP_SERVER_URL}/ticket_summary", json=payload)
    r.raise_for_status()
    return r.json()

@tool
def usage_report(account_id: str, month: str) -> dict:
    """
    Calls MCP server to generate usage report for the account_id for the given month.
    """
    payload = {"account_id": account_id, "month": month}
    r = requests.post(f"{MCP_SERVER_URL}/usage_report", json=payload)
    r.raise_for_status()
    return r.json()

@tool
def kb_search(query: str, k: int = 5) -> dict:
    """
    Calls MCP server knowledge base search endpoint with query, returns top k results.
    """
    payload = {"query": query, "k": k}
    # print("tools kb search payload", payload)
    r = requests.post(f"{MCP_SERVER_URL}/kb_search", json=payload)
    r.raise_for_status()
    return r.json()

llm = ChatOpenAI(temperature=0)

parameter_output_parser = PydanticOutputParser(pydantic_object=QueryParameters)
parameter_extraction_template = """
Extract the invoice_id, account_id, ticket_id and period from the following user query.
Return a JSON object with keys: invoice_id, account_id, ticket_id, period.
If a field is not mentioned, set its value to null.

Query: {query}
"""
parameter_extraction_prompt = ChatPromptTemplate.from_template(parameter_extraction_template)
parameter_extraction_chain = LLMChain(
    llm=llm,
    prompt=parameter_extraction_prompt,
    output_parser=parameter_output_parser,
)

def router(state: AgentState) -> AgentState:
    """
    Determine intent from user query.
    """
    q = state.query.lower()
    if "invoice" in q or "account" in q or "usage" in q or "ticket" in q:
        state.intent = "DataLookup"
    elif "how to" in q or "faq" in q or "help" in q:
        state.intent = "FAQ"
    else:
        state.intent = "Escalation"
    # print("router state", state)
    return state

def extract_parameters(state: AgentState) -> AgentState:
    """
    Extract structured query parameters from raw user query using LLM chain.
    """
    result = parameter_extraction_chain.invoke({"query": state.query})
    # print("Extracted params", result)
    # Some output parsers (incl. PydanticOutputParser) nest the parsed object under 'text'
    if isinstance(result, dict):
        if 'text' in result and isinstance(result['text'], QueryParameters):
            state.query_params = result['text']
        elif 'text' in result and isinstance(result['text'], dict):
            state.query_params = QueryParameters(**result['text'])
        else:
            # fallback: try to construct QueryParameters from dict
            state.query_params = QueryParameters(**result)
    elif isinstance(result, QueryParameters):
        state.query_params = result
    else:
        state.query_params = QueryParameters()
    # print("Assigned params:", state.query_params)
    return state

def retrieve(state: AgentState) -> AgentState:
    """
    Query knowledge base using kb_search.
    """
    result = kb_search.invoke({"query": state.query, "k": 5})
    val = result.get("result", "")
    print("graph - retrieve kb search")
    if isinstance(val, (list, dict)):
        state.answer = str(val)
    else:
        state.answer = val
    state.evidence.append(result.get("source", ""))
    return state

def tools(state: AgentState) -> AgentState:
    """
    Call MCP tools with extracted parameters for data lookup.
    """
    params = state.query_params or QueryParameters()
    print("tools params", params)
    invoice_id = params.invoice_id
    account_id = params.account_id or "None"  # Default/fallback should match your real data
    ticket_id = params.ticket_id
    period = params.period

    if invoice_id:
        response = invoice_status.invoke({"account_id": account_id, "invoice_id": invoice_id})
    elif account_id and account_id.lower() != 'none':
        # print("inside account")
        response = account_lookup.invoke({"account_id": account_id})
    elif ticket_id:
        # print("inside ticket")
        response = ticket_summary.invoke({"ticket_id": ticket_id})
    else:
        response = {"result": "Insufficient parameters to perform lookup.", "source": ""}

    val = response.get("result", "")
    if isinstance(val, (list, dict)):
        state.answer = str(val)
    else:
        state.answer = val
    state.evidence.append(response.get("source", ""))
    return state


def synthesize(state: AgentState) -> AgentState:
    """
    Compose final answer with evidence details.
    """
    if state.evidence:
        state.answer = (state.answer or "Here's what I found. Answer you are looking for are available with references presented as evidence") + "\n\nEvidence:\n" + "\n".join([str(e) for e in state.evidence if e])
    else:
        state.answer = (state.answer or "")
    return state

# def synthesize(state: AgentState) -> AgentState:
#     """
#     Compose final answer with evidence details.
#     """
#     if state.evidence:
#         combined = "\n\n".join([e.get("snippet", "") if isinstance(e, dict) else str(e) for e in state.evidence])
#         state.answer = f"Here is what I found on your query:\n{combined}"
#     else:
#         state.answer = "Sorry, I could not find relevant information."
#     return state

# def synthesize(state: AgentState) -> AgentState:
#     if state.evidence:
#         details = []
#         for record in state.evidence:
#             if isinstance(record, dict):
#                 summary = ", ".join(f"{k}: {v}" for k, v in record.items())
#                 details.append(summary)
#             else:
#                 details.append(str(record))
#         state.answer = f"Here are the details:\n" + "\n".join(details)
#     else:
#         # If no evidence fallback to prior message or polite denial
#         state.answer = state.answer or "Sorry, I could not find relevant information."
#     return state


def escalate(state: AgentState) -> AgentState:
    """
    Fallback escalation node.
    """
    state.answer = "Sorry, could not handle your request. Escalating to human support."
    return state

def route_decision(state: AgentState):
    """
    Route based on intent.
    """
    return state.intent

graph = StateGraph(AgentState)

graph.add_node("router", router)
graph.add_node("extract_params", extract_parameters)
graph.add_node("FAQ", retrieve)
graph.add_node("DataLookup", tools)
graph.add_node("synthesize", synthesize)
graph.add_node("Escalation", escalate)

graph.add_edge("router", "extract_params")

graph.add_conditional_edges("extract_params", route_decision, {
    "FAQ": "FAQ",
    "DataLookup": "DataLookup",
    "Escalation": "Escalation"
})

graph.add_edge("FAQ", "synthesize")
graph.add_edge("DataLookup", "synthesize")
graph.add_edge("synthesize", END)
graph.add_edge("Escalation", END)

graph.set_entry_point("router")

compiled_agent = graph.compile()
