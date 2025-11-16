from langchain_mcp import MCPToolkit

def get_all_tools():
    pdf_toolkit = MCPToolkit.from_server("pdf-server")
    csv_toolkit = MCPToolkit.from_server("csv-server")
    db_toolkit  = MCPToolkit.from_server("db-server")
    email_toolkit = MCPToolkit.from_server("email-server")

    return (
        pdf_toolkit.get_tools() +
        csv_toolkit.get_tools() +
        db_toolkit.get_tools() +
        email_toolkit.get_tools()
    )
