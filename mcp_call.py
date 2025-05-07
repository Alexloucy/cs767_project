import mcp
from mcp.client.websocket import websocket_client
import json
import base64
import os

config = {}
# Encode config in base64
config_b64 = base64.b64encode(json.dumps(config).encode())
smithery_api_key = "your-api-key"

# Create server URL
url = f"wss://server.smithery.ai/@nickclyde/duckduckgo-mcp-server/ws?config={config_b64}&api_key={os.getenv('smithery_api_key')}"

async def call_DuckDuckGo_search(query):
    # Connect to the server using websocket client
    async with websocket_client(url) as streams:
        async with mcp.ClientSession(*streams) as session:
            # Initialize the connection
            await session.initialize()
            # List available tools
            tools_result = await session.list_tools()
            # print(f"Available tools: {', '.join([t.name for t in tools_result.tools])}")

            # Example of calling a tool:
            result = await session.call_tool("search", arguments={"query": query})
            print(f"Tool call result: {result.content}")
            return result.content

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())