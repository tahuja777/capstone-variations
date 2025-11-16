import requests

class MCPClient:
    """
    A lightweight client to communicate with the MCP Tool Server.
    """
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url

    def call_tool(self, tool_name, payload):
        """
        Send a POST request to the MCP Tool Server to invoke a specific tool.
        """
        url = f"{self.base_url}/tools/{tool_name}"
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "tool_name": tool_name}
