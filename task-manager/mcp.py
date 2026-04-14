from mcp import Client

client = Client(config=".vscode/mcp.json")

tools = client.list_tools()
print (tools)
result = client.invoke_tool(
    name="security-scan",
    arguments={
        "path": "."
    }
)

print(result)