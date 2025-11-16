from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
import sqlite3

from app.state import NovaState
from app.nodes.router_node import router_node
from app.nodes.tools_node import tools_node
from app.nodes.synthesize_node import synthesize_node

from app.utils.prompt_loader import (
    load_router_prompt,
    load_tool_prompt,
    load_synthesis_prompt
)

# checkpointer import
from langgraph.checkpoint.sqlite import SqliteSaver


# Loading environment variables if missing
load_dotenv()

# LLM setup
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

# Load prompt templates
router_prompt = load_router_prompt()
tool_prompt = load_tool_prompt()
synthesis_prompt = load_synthesis_prompt()

# Build graph
graph = StateGraph(NovaState)

# Add nodes
graph.add_node("router", lambda s: router_node(s, llm, router_prompt))
graph.add_node("tools", lambda s: tools_node(s, llm, tool_prompt))
graph.add_node("synthesis", lambda s: synthesize_node(s, llm, synthesis_prompt))

# Set entry point
graph.set_entry_point("router")

# Conditional edge based on intent
graph.add_conditional_edges(
    "router",
    lambda state: state.intent,
    {
        "invoice": "tools",
        "ticket": "tools",
        "account": "tools",
        "usage": "tools",
        "Unknown": "synthesis"
    }
)

# Edge connections
graph.add_edge("tools", "synthesis")
graph.add_edge("synthesis", END)

# Use SQLite connection
conn = sqlite3.connect("memory.sqlite", check_same_thread=False)  # Establish the connection
checkpointer = SqliteSaver(conn)  # Pass the connection, not the string

# Compile graph with checkpointer
compiled_graph = graph.compile(checkpointer=checkpointer)


# Runner
def run_query(query: str):
    print(f"\n--- Processing Query: '{query}' ---\n")

    config = {"thread_id": "demo-thread"}

    # Using the 'stream' method with the compiled graph
    for event in compiled_graph.stream({"query": query}, config=config):
        print("STREAM:", event)

    # Final invocation of the graph
    result = compiled_graph.invoke({"query": query}, config=config)

    print("\nFINAL RESULT:", result)
    return result


if __name__ == "__main__":
    run_query("Show my invoice for august month")
    run_query("Check and tell me the invoice number that has highest amount with status paid")
