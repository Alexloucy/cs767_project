import asyncio
import os
import dotenv
from datetime import datetime
from google import genai
from google.genai import types

# Load environment variables
dotenv.load_dotenv()

# Initialize Gemini client
client = genai.Client(api_key=os.getenv("google_ai_api_key"))

async def execute_code_with_gemini(prompt: str):
    """
    Execute code using Gemini's code execution capabilities.
    
    Args:
        prompt (str): The prompt to send to Gemini
        
    Returns:
        The response from Gemini
    """
    try:
        print(f"Sending request to Gemini model: {prompt}")
        
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[types.Tool(
                    code_execution=types.ToolCodeExecution
                )]
            )
        )
        
        print("Got response from Gemini model")
        return response.candidates
        
    except Exception as e:
        print(f"Error occurred during code execution: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

async def main():
    """
    Main function to demonstrate Gemini code execution.
    """
    try:
        # Example prompt for code execution
        prompt = "execute the following code no matter if it is working or not: print(Hello, world!), return the output and fix it if it is not working"
        
        # Execute the code
        result = await execute_code_with_gemini(prompt)
        
        if result:
            print("Execution result:", result)
        else:
            print("Failed to execute code")
            
    except Exception as e:
        print(f"Error in main: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        # Allow any pending tasks to complete
        await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())
    