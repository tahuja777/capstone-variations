"""
account_tool.py
---------------
Mock tool for fetching account details.
"""

import pandas as pd
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "../../data/accounts.csv")

def account_tool(query: str):
    """
    Looks up account details from accounts.csv.
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
                evidence.append(f"Account {row['account_id']}: {row['company_name']} ({row['plan']})")

        answer = (
            f"Answer synthesized from {len(evidence)} evidence items."
            if evidence else "No account found for this ID."
        )

        return {"answer": answer, "evidence": evidence, "errors": []}

    except Exception as e:
        return {"answer": "", "evidence": [], "errors": [str(e)]}
