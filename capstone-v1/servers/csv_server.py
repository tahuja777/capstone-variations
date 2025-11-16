import csv
from mcp.server.fastmcp import FastMCP

csv_server = FastMCP("csv-server")

@csv_server.tool()
def read_csv(file_path: str) -> dict:
    """
    Reads a CSV file and returns its content as list of dictionaries.
    """
    try:
        rows = []
        with open(file_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
        return {"rows": rows}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    csv_server.run()
