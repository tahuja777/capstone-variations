# app/utils/prompt_loader.py

def load_router_prompt() -> str:
    """ Load the router prompt from file """
    return load_prompt('app/prompts/router_prompt.txt')

def load_tool_prompt() -> str:
    """ Load the tool prompt from file """
    return load_prompt('app/prompts/tool_prompt.txt')

def load_synthesis_prompt() -> str:
    """ Load the synthesis prompt from file """
    return load_prompt('app/prompts/synthesis_prompt.txt')

def load_prompt(file_path: str) -> str:
    """
    This function reads a prompt file and returns the content as a string.
    """
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return ""
