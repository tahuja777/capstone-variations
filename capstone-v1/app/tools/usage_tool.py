"""
usage_tool.py
-------------
Mock tool for usage reports.
"""

import pandas as pd
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "../../data/usage.csv")

def usage_tool(query: str):
    """
    Returns usage data summary for a given account.
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
                evidence.append(f"Usage report {row['month']}: {row['usage_units']} units used")

        answer = (
            f"Answer synthesized from {len(evidence)} evidence items."
            if evidence else "No usage data found for this account."
        )

        return {"answer": answer, "evidence": evidence, "errors": []}

    except Exception as e:
        return {"answer": "", "evidence": [], "errors": [str(e)]}
