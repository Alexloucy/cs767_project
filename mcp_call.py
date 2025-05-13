import mcp
from mcp.client.streamable_http import streamablehttp_client
import json
import base64
import os

config = {}
config = {"braveApiKey": os.getenv("BRAVE_API_KEY")}
# Encode config in base64
config_b64 = base64.b64encode(json.dumps(config).encode())
smithery_api_key = os.getenv("SMITHERY_API_KEY")

# Create server URL
# url = f"https://server.smithery.ai/@nickclyde/duckduckgo-mcp-server/mcp?config={config_b64}&api_key={smithery_api_key}"
url = f"https://server.smithery.ai/@smithery-ai/brave-search/mcp?config={config_b64}&api_key={smithery_api_key}"


async def call_DuckDuckGo(query):
    # Connect to the server using HTTP client
    async with streamablehttp_client(url) as (read_stream, write_stream, _):
        async with mcp.ClientSession(read_stream, write_stream) as session:
            # Initialize the connection
            await session.initialize()
            # List available tools
            tools_result = await session.list_tools()
            result = await session.call_tool("brave_web_search", arguments={"query": query, "count": 3})
            print([content.text for content in result.content])
            return [content.text for content in result.content]

if __name__ == "__main__":
    import asyncio
    asyncio.run(call_DuckDuckGo("What is the capital of France?"))