import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "capstone" / "data" / "accounts.csv"

def account_lookup(account_id: str | None = None, company: str | None = None):
    df = pd.read_csv(DATA_PATH)

    if account_id:
        record = df[df["account_id"].astype(str) == str(account_id)]
    elif company:
        record = df[df["company"].str.lower() == company.lower()]
    else:
        return {"error": "Please provide either account_id or company."}

    if record.empty:
        return {"error": "No account found with given parameters."}

    row = record.iloc[0].to_dict()
    explanation = f"Account details fetched for {row.get('company')}."
    source = f"accounts.csv: row {record.index[0]}"

    return {
        "data": row,
        "explanation": explanation,
        "source": source
    }
