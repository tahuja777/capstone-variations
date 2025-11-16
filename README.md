# capstone-variations
Agentic Training Assignment

# capstone v0
#### This is an H4 Heading
Application status: 
Work in progress

This folder contains the initial version of the application. In this version you will find below implementations.
*Setp up LLM
*Chains
*Tools setup
*Router Setup
*MCP server setup
*All paths setup in MCP server for calling individual tool service
*CSV reading logic
*CLI setup

#### This is an H4 Heading
What is missing:
*Remembering the turns conversation
*Vector DB implementation

#### This is an H4 Heading
How to run application
*Entry path is /app/cli.py
*Ensure server is running inside the path
    * app/servers/mcp_nova/server.py

#### This is an H4 Heading
Tested below queries.
*Tell me all information about the invoice with id INV-A001-3
*Tell me all information about the invoice with id INV-A006-3
*Tell me all information about the invoice with account id A005 and invoice id INV-A005-1
*I need help with pricing plans
*I need help with Pricing & Plans
*I need help with novacrm offers
*I need help with billing
*Can you explain how to resolve secure information using AES-256



# capstone v1
#### This is an H4 Heading
Application status:
Work in progress

This folder contains the more advanced setup of the project. I tried to achieve more modular strucutre compared to previous one capstone-0.

#### This is an H4 Heading
What is covered
*Setp up LLM
*Chains
*Tools setup
*Router Setup
*MCP server setup
*Reading mock data from MCP server
*Faiss Index
*Remembering the turns conversation (Maintaining history)

#### This is an H4 Heading
What is missing
*CSV reading logic
*Proper setup of reading KB documents.

#### This is an H4 Heading
How to run application
*Entry path is /app/graph_agent.py
*Ensure server is running inside the path
    * app/servers/mcp_nova/server.py