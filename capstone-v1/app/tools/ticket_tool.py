"""
ticket_tool.py
--------------
Mock tool for ticket summaries.
"""

import pandas as pd
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "../../data/tickets.csv")

def ticket_tool(query: str):
    """
    Fetches open tickets from tickets.csv for a given account.
    """
    try:
        df = pd.read_csv(os.path.abspath(DATA_PATH))
        account_id = None
        for word in query.split():
            if word.isdigit():
                account_id = word
                break

        evidence = []
        if account_id:
            matched = df[df["account_id"].astype(str) == account_id]
            for _, row in matched.iterrows():
                evidence.append(f"Ticket {row['ticket_id']}: {row['status']} since {row['created_at']}")

        answer = (
            f"Answer synthesized from {len(evidence)} evidence items."
            if evidence else "No tickets found for this account."
        )

        return {"answer": answer, "evidence": evidence, "errors": []}

    except Exception as e:
        return {"answer": "", "evidence": [], "errors": [str(e)]}
