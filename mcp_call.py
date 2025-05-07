import asyncio
import smithery
import mcp
import os
from mcp.client.websocket import websocket_client
import dotenv
from datetime import datetime
from google import genai
from google.genai import types
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

dotenv.load_dotenv()

# Create Smithery URL with server endpoint
url = smithery.create_smithery_url("wss://server.smithery.ai/@smithery-ai/brave-search/ws", {
  "braveApiKey": os.getenv('brave_api_key')
}) + f"&api_key={os.getenv('smithery_api_key')}"

client = genai.Client(api_key=os.getenv("google_ai_api_key"))

chat = client.chats.create(
    model='gemini-2.0-flash',
    config=types.GenerateContentConfig(
      tools=[types.Tool(
        code_execution=types.ToolCodeExecution
      )]
    )
)

# Create server parameters for stdio connection
# brave_server_params = StdioServerParameters(
#     command="npx",
#     args=["-y", "@modelcontextprotocol/server-brave-search"],
#     env={
#         "BRAVE_API_KEY": os.getenv('brave_api_key')
#       },
# )

server_params = StdioServerParameters(
    command="npx",  # Executable
    args=["-y", "@philschmid/weather-mcp"],  # Weather MCP Server
    env=None,  # Optional environment variables
)

async def getToolSmithery():
    # Connect to the server using websocket client
    async with websocket_client(url) as streams:
        async with mcp.ClientSession(*streams) as session:
            # List available tools
            tools_result = await session.list_tools()
            # print(tools_result)
            for tool in tools_result.tools:
                print(tool)
          
            result = await session.call_tool("brave_web_search", {"query": "What is the weather in Tokyo?"})
            print(result)
            # Example: Call a tool
            # result = await session.call_tool("tool_name", {"param1": "value1"})
            # Example: Call a tool
            # result = await session.call_tool("tool_name", {"param1": "value1"})
            return tools_result.tools

async def run():
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Prompt to get the weather for the current day in London.
                prompt = f"What is the weather in London in {datetime.now().strftime('%Y-%m-%d')}?"
                print(prompt)

                print("Sending request to Gemini model...")
                response = client.models.generate_content(
                    model='gemini-2.0-flash',
                    contents='What is the sum of the first 50 prime numbers? '
                            'Generate and run code for the calculation, and make sure you get all 50.',
                    config=types.GenerateContentConfig(
                        tools=[types.Tool(
                        code_execution=types.ToolCodeExecution
                        )]
                    )
                )
                print("Got response from Gemini model", response.candidates)
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        # Ensure any remaining resources are cleaned up
        await asyncio.sleep(0)  # Allow any pending tasks to complete

if __name__ == "__main__":
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        # Ensure the event loop is closed
        loop = asyncio.get_event_loop()
        if loop.is_running():
            loop.stop()
        if not loop.is_closed():
            loop.close()

# if __name__ == "__main__":
#     asyncio.run(getToolSmithery())
