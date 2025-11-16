import os
import pandas as pd
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "invoices.csv")

def invoice_lookup(invoice_id: str | None = None, account_id: str | None = None, period: str | None = None):
    """
    Look up invoices by invoice_id, account_id, or period date (DD-MM-YYYY).
    """
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"invoices.csv not found at {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)
    df.columns = df.columns.str.strip().str.lower()
    df["account_id"] = df["account_id"].astype(str).str.strip()

    # Apply filters
    if invoice_id:
        df = df[df["invoice_id"].astype(str).str.lower() == str(invoice_id).lower()]

    if account_id:
        df = df[df["account_id"].str.lower() == account_id.lower()]

    # WIP
    # if period:
    #     try:
    #         period_date = pd.to_datetime(period, dayfirst=True)
    #         df = df[(df["period_start"] <= period_date) & (df["period_end"] >= period_date)]
    #     except Exception as e:
    #         raise ValueError(f"Invalid period format '{period}'. Expected DD-MM-YYYY. Details: {e}")

    return df.to_dict(orient="records")
