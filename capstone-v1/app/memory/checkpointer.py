from langgraph.checkpoint.sqlite import SqliteSaver

def get_checkpointer():
    return SqliteSaver("memory.db")
