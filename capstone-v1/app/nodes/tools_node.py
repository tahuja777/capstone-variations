# app/nodes/tools_node.py

from app.utils.call_tools import call_tool

def tools_node(state, llm, tool_prompt):
    """
    Executes the appropriate tool based on detected intent.
    """
    intent = state.intent
    query = state.query

    # Build final prompt (must use the escaped JSON prompt provided earlier)
    prompt = tool_prompt.format(query=query, intent=intent)

    # LLM response
    llm_response = llm.invoke(prompt)
    tool_call = llm_response.content

    # Execute tool based on intent and response from tool_call
    tool_result = call_tool(intent, tool_call)

    # Save in state
    state.tool_result = tool_result

    return state
