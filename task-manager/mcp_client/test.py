from mcp.client import Client

client = Client(["npx", "-y", "opsera"])
print (client)

# 🔍 List available tools
tools = client.list_tools()
print("Available tools:", tools)

# 🔐 Call security scanner
result = client.call_tool(
    "security-scan",
    {
        "path": "./",
        "scan_type": "full"
    }
)

print("Scan Result:", result)

client.close()