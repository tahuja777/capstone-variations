def router_node(state):
    query = state["input"]

    if "csv" in query.lower():
        return "csv"

    if "pdf" in query.lower():
        return "pdf"

    if "email" in query.lower():
        return "email"

    return "unknown"
