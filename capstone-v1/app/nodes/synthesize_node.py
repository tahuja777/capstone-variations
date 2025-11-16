# app/nodes/synthesize_node.py

def synthesize_node(state, llm, synthesis_prompt):
    print("\n[SYNTHESIZE NODE] Synthesizing final response...")

    tool_output = state.tool_result

    # Build the synthesis prompt safely
    prompt = synthesis_prompt.format(
        query=state.query,
        intent=state.intent,
        tool_answer=tool_output.get("result") if tool_output else "No tool result",
    )

    # Generate final answer from LLM
    response = llm.invoke(prompt).content

    # Store the final answer
    state.answer = response

    # Clean memory
    state.history = [response]

    return state
