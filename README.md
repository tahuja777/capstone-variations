# capstone-variations
Agentic Training Assignment

# capstone v0
Application status: Work in progress

This folder contains the initial version of the application. In this version you will find below implementations.
-Setp up LLM
-Chains
-Tools setup
-Router Setup
-MCP server setup
-All paths setup in MCP server for calling individual tool service
-CSV reading logic

What is missing:
-Remembering the turns conversation
-Vector DB implementation

How to run application
-Entry path is /app/cli.py
-Ensure server is running inside the path
    - app/servers/mcp_nova/server.py

Tested below queries.

# capstone v1
Application status: Work in progress

This folder contains the more advanced setup of the project. I tried to achieve more modular strucutre compared to previous one capstone-0.
What is covered
-Setp up LLM
-Chains
-Tools setup
-Router Setup
-MCP server setup
-Reading mock data from MCP server
-Faiss Index
-Remembering the turns conversation (Maintaining history)

What is missing
-CSV reading logic
-Proper setup of reading KB documents.