from fastapi import FastAPI, Query
from project_tools import account, invoice, ticket, usage

app = FastAPI(title="NovaCRM MCP Server")


@app.get("/account_lookup")
def account_lookup(account_id: str | None = Query(None), company: str | None = Query(None)):
    return account.account_lookup(account_id, company)


@app.get("/invoice_lookup")
def invoice_lookup(account_id: str, invoice_id: str | None = Query(None), period: str | None = Query(None)):
    return invoice.invoice_lookup(account_id=account_id, invoice_id=invoice_id, period=period)


@app.get("/ticket_summary")
def ticket_summary(account_id: str, window_days: int = 90):
    return ticket.ticket_summary(account_id, window_days)


@app.get("/usage_report")
def usage_report(account_id: str, month: str):
    return usage.usage_report(account_id, month)

# WIP
# @app.get("/kb_search")
# def kb_search(query: str, k: int = 5):
#     # This will later integrate with FAISS RAG retriever
#     return {"query": query, "results": [], "source": "index/faiss_index.bin"}
