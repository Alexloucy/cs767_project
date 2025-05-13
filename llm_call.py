import asyncio
import os
import dotenv
from datetime import datetime
from google import genai
from google.genai import types
from pydantic import BaseModel

class Search_Result(BaseModel):
    answer: str
    feedback: str
    problem: str
    need_improve: bool

class Code_Reflect(BaseModel):
    answer: int
    feedback: str
    problem: str
    need_improve: bool

# Load environment variables
dotenv.load_dotenv()

# Initialize Gemini client
client = genai.Client(api_key=os.getenv("google_ai_api_key"))

async def call_llm(prompt: str, isCode: bool = False, isReflection = False, summerize: bool = False) -> str:
    """
    Execute code using Gemini's code execution capabilities.
    
    Args:
        prompt (str): The prompt to send to Gemini
        
    Returns:
        The response from Gemini
    """
    
    try:
        response = None
        if (isCode):
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    tools=[types.Tool(
                        code_execution=types.ToolCodeExecution
                    )],
                    temperature=0
                )
            )
            return response
        elif (isReflection):
            reflection_prompt = f"""{prompt}"""
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=reflection_prompt,
                config=types.GenerateContentConfig(
                    temperature=0,
                    response_schema=Code_Reflect,
                    response_mime_type="application/json",
                    max_output_tokens=500
                )
            )
            return response.text
        elif (summerize):
            reflection_prompt = "\n".join(prompt)
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents= "summarize the following reflection to one sentence less than 50 words. Don't focus on the specific case, generalize it so that it can be applied to other similar questions. \n" + reflection_prompt,
                config=types.GenerateContentConfig(
                    temperature=0,
                )
            )
            print("summerize response:", response.text)
            return response.text
        else:
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt + " output the answer only",
                config=types.GenerateContentConfig(
                    temperature=0,
                    response_schema=Search_Result,
                    response_mime_type="application/json",
                    max_output_tokens=500
                )
            )
            return response.text
        
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
        prompt = "write a python function that calculates the sum of numbers from 1 to 10, in your response, include the code and the output of the code execution"
        
        # Execute the code
        result = await call_llm(prompt)
        
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

