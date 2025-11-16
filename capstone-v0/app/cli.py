# cli.py

from graph import compiled_agent, AgentState
from rich.console import Console

def main():
    console = Console()
    console.print("[bold cyan]NovaCRM AI Assistant CLI[/bold cyan]")
    history = []
    while True:
        query = input("User: ")
        if query.lower() in ["exit", "quit"]:
            break
        state = AgentState(query=query, history=history)
        final_state = compiled_agent.invoke(state)
        history.append(query)
        console.print(f"[bold green]Assistant:[/bold green]\n{final_state['answer']}")
        if final_state.get("evidence"):
            console.print("[bold yellow]Evidence:[/bold yellow] " + ", ".join(final_state["evidence"]))
        if final_state.get("errors"):
            console.print("[bold red]Errors:[/bold red] " + ", ".join(final_state["errors"]))

if __name__ == "__main__":
    main()
