# app/servers/invoice_server.py

import csv
import json
from mcp.server.fastmcp import FastMCP

server = FastMCP("invoice_server")


@server.tool()
def get_invoice_details(month: str) -> dict:
    """
    Lookup invoice by month from invoices.csv
    """
    csv_path = "invoices.csv"
    results = []

    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["month"].lower() == month.lower():
                results.append(row)

    return {"invoices": results}


@server.tool()
def get_highest_paid_invoice() -> dict:
    """
    Returns invoice with maximum amount having status 'paid'
    """
    csv_path = "invoices.csv"
    highest = None

    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["status"].lower() == "paid":
                if highest is None or float(row["amount"]) > float(highest["amount"]):
                    highest = row

    return {"invoice": highest}


if __name__ == "__main__":
    server.run()
