# capstone/servers/mcp_nova/server.py

from flask import Flask, request, jsonify
import pandas as pd
from thefuzz import fuzz
import os
import glob

app = Flask(__name__)
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data"))
KB_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../kb"))

def load_csv(file):
    path = os.path.join(DATA_DIR, file)
    return pd.read_csv(path)

@app.route("/account_lookup", methods=["POST"])
def account_lookup():
    """
    Looks up account information by account_id or company, using exact fields in account.csv.
    """
    data = request.json
    account_id = data.get("account_id")
    company = data.get("company")

    df = load_csv("accounts.csv")

    filtered = pd.DataFrame()
    if account_id:
        # Normalize for robust matching (strip spaces, case-insensitive)
        filtered = df[df["account_id"].astype(str).str.strip().str.upper() == account_id.strip().upper()]
    elif company:
        filtered = df[df["company"].astype(str).str.strip().str.upper() == company.strip().upper()]

    # Results as list of dicts for JSON
    records = filtered.to_dict(orient="records")
    return jsonify({
        "result": records,
        "source": f"accounts.csv rows: {list(filtered.index)}"
    })

@app.route("/invoice_status", methods=["POST"])
def invoice_status():
    data = request.json
    account_id = data.get("account_id")
    invoice_id = data.get("invoice_id")

    invoices = load_csv("invoices.csv")

    filtered = invoices

    # print("account_id inside server invoice", account_id)
    if invoice_id and invoice_id.lower() != 'none':
        filtered = filtered[invoices["invoice_id"].str.strip().str.upper() == invoice_id.strip().upper()]
    if account_id and account_id.lower() != 'none':
        # print("checking accounts as well inside invoice look up")
        filtered = filtered[filtered["account_id"].str.strip().str.upper() == account_id.strip().upper()]
    # print("invoice filtered", filtered)
    # If filtered DataFrame is empty, return sensible empty result instead of causing server error
    if filtered.empty:
        return jsonify({
            "result": [],
            "source": "invoices.csv rows: []"
        })

    # Otherwise, safely convert and return the matching rows
    records = filtered.to_dict(orient="records")
    return jsonify({
        "result": records,
        "source": f"invoice.csv rows: {list(filtered.index)}"
    })


@app.route("/ticket_summary", methods=["POST"])
def ticket_summary():
    data = request.json
    tickets = load_csv("tickets.csv")
    ticket = tickets[tickets["ticket_id"] == data["ticket_id"]]
    expl = ticket.to_dict(orient="records")
    return jsonify({"explanation": expl, "source": "tickets.csv rows: " + str(ticket.index.tolist())})

@app.route("/usage_report", methods=["POST"])
def usage_report():
    data = request.json
    usage = load_csv("usage.csv")
    report = usage[(usage["account_id"] == data["account_id"]) & (usage["month"] == data["month"])]
    expl = report.to_dict(orient="records")
    return jsonify({"explanation": expl, "source": "usage.csv rows: " + str(report.index.tolist())})


@app.route("/kb_search", methods=["POST"])
def kb_search():
    query = request.json.get("query", "").lower()
    print("kb_search query", query)
    k = request.json.get("k", 5)
    KB_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../kb"))
    docs = glob.glob(os.path.join(KB_DIR, "*.md"))
    print("server kb docs", docs)

    scored_docs = []
    for doc in docs:
        with open(doc, "r", encoding="utf-8") as f:
            content = f.read().lower()
            # Compute fuzzy similarity between query and content snippet or filename
            score = max(fuzz.partial_ratio(query, content[:500]), fuzz.partial_ratio(query, os.path.basename(doc).lower()))
            if score > 50:  # threshold for match
                scored_docs.append({"file": os.path.basename(doc), "snippet": content[:200], "score": score})

    scored_docs.sort(key=lambda x: x["score"], reverse=True)
    matches = scored_docs[:k]

    return jsonify({
        "explanation": matches,
        "source": "kb/ files: " + str([m['file'] for m in matches])
    })


if __name__ == "__main__":
    app.run(port=8000)
