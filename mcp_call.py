import os
import mcp
from mcp.client.streamable_http import streamablehttp_client
import json
import base64
import asyncio

config = {
  "braveApiKey": os.getenv("brave_api_key"),
}
# Encode config in base64
config_b64 = base64.b64encode(json.dumps(config).encode())
smithery_api_key = os.getenv("smithery_api_key")

# Create server URL
url = f"https://server.smithery.ai/@smithery-ai/brave-search/mcp?config={config_b64}&api_key={smithery_api_key}"

async def main():
    # Connect to the server using HTTP client
    async with streamablehttp_client(url) as streams:
        async with mcp.ClientSession(*streams) as session:
            # Initialize the connection
            await session.initialize()
            # List available tools
            tools_result = await session.list_tools()
            print(f"Available tools: {', '.join([t.name for t in tools_result.tools])}")

if __name__ == "__main__":

    asyncio.run(main())