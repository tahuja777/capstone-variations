import os
import pandas as pd
from datetime import datetime, timedelta

# Base directory resolution
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "tickets.csv")

def ticket_summary(account_id: str, window_days: int = 90):
    """
    Summarize tickets for a given account_id within the last 'window_days' days
    based on the 'opened_on' date.
    Example: /ticket_summary?account_id=A001&window_days=90
    """
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"tickets.csv not found at {DATA_PATH}")

    # Read the CSV file
    df = pd.read_csv(DATA_PATH)

    # Normalize column names and data
    df.columns = df.columns.str.strip().str.lower()
    df["account_id"] = df["account_id"].astype(str).str.strip()
    df["status"] = df["status"].astype(str).str.strip().str.title()
    df["priority"] = df["priority"].astype(str).str.strip().str.title()

    # Convert opened_on to datetime
    df["opened_on"] = pd.to_datetime(df["opened_on"], dayfirst=True, errors="coerce")

    # Filter by account_id and time window
    end_date = datetime.today()
    start_date = end_date - timedelta(days=window_days)

    filtered_df = df[
        (df["account_id"].str.lower() == account_id.lower())
        & (df["opened_on"] >= start_date)
        & (df["opened_on"] <= end_date)
    ]

    # Compute metrics
    total_tickets = len(filtered_df)
    status_counts = filtered_df["status"].value_counts().to_dict()
    priority_counts = filtered_df["priority"].value_counts().to_dict()

    # Prepare summary
    summary = {
        "account_id": account_id,
        "window_days": window_days,
        "total_tickets": total_tickets,
        "status_summary": status_counts,
        "priority_summary": priority_counts,
        "tickets": filtered_df.to_dict(orient="records")
    }

    return summary
