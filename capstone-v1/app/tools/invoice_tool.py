"""
invoice_tool.py
---------------
Mock tool for handling invoice-related queries.
Simulates reading from invoices.csv dataset.
"""

import pandas as pd
import os

# Path to data file (adjust if needed)
DATA_PATH = os.path.join(os.path.dirname(__file__), "../../data/invoices.csv")

def invoice_tool(query: str):
    """
    Simulates fetching invoice info from the dataset.
    """
    try:
        df = pd.read_csv(os.path.abspath(DATA_PATH))
        # simple logic: look for "account" ID in query
        account_id = None
        for word in query.split():
            if word.isdigit():
                account_id = word
                break

        evidence = []
        if account_id:
            matched = df[df["account_id"].astype(str) == account_id]
            for _, row in matched.iterrows():
                evidence.append(f"Invoice {row['invoice_id']}: {row['status']} on {row['date']}")

        answer = (
            f"Answer synthesized from {len(evidence)} evidence items."
            if evidence else "No invoice found for this account."
        )

        return {"answer": answer, "evidence": evidence, "errors": []}

    except Exception as e:
        return {"answer": "", "evidence": [], "errors": [str(e)]}
