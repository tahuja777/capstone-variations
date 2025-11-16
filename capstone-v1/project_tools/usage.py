import os
import pandas as pd

# Base directory safe resolution
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "usage.csv")

def usage_report(account_id: str, month: str):
    """
    Generate usage report for a specific account and month.
    Example: /usage_report?account_id=A001&month=2025-09
    """
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"usage.csv not found at {DATA_PATH}")

    # Load data
    df = pd.read_csv(DATA_PATH)

    # Normalize column names and strip spaces
    df.columns = df.columns.str.strip().str.lower()
    df["account_id"] = df["account_id"].astype(str).str.strip()
    df["month"] = df["month"].astype(str).str.strip()

    # Filter based on account_id and month
    filtered_df = df[
        (df["account_id"].str.lower() == account_id.lower()) &
        (df["month"] == month)
    ]

    if filtered_df.empty:
        return {
            "account_id": account_id,
            "month": month,
            "message": "No usage data found for the given account and month."
        }

    # Extract usage metrics
    record = filtered_df.iloc[0]
    report = {
        "account_id": record["account_id"],
        "month": record["month"],
        "api_calls": int(record["api_calls"]),
        "email_sends": int(record["email_sends"]),
        "storage_gb": float(record["storage_gb"]),
    }

    # Optionally computing percentage usage if we have thresholds
    THRESHOLDS = {"api_calls": 500000, "email_sends": 100000, "storage_gb": 200}
    utilization = {
        metric: round((report[metric] / THRESHOLDS[metric]) * 100, 2)
        for metric in THRESHOLDS
    }

    report["utilization_percent"] = utilization

    return report
