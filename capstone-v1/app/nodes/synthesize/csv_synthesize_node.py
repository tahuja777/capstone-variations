from langchain_core.messages import ToolMessage
from langchain_mcp import MCPToolkit

csv_toolkit = MCPToolkit.from_server("csv-server")
read_csv_tool = csv_toolkit.get_tools()[0]

def csv_synthesize_node(state):
    file_path = state["file_path"]

    result = read_csv_tool.invoke({"file_path": file_path})

    state["history"].append(
        ToolMessage(
            content=f"CSV content extracted: {result}",
            tool="csv-server:read_csv"
        )
    )

    return {
        "output": result,
        "history": state["history"]
    }
