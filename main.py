import pandas as pd
import json
from llm_call import call_llm
import random
import asyncio

def read_jsonl(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))
    return data

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_tool_examples():
    with open('prompt/tool.md', 'r') as f:
        return f.read()
    

def combine_datasets():
    # Read datasets
    gsm_data = read_jsonl('dataset/gsm.jsonl')
    web_data = read_json('dataset/verified-web-dev.json')
    
    # Convert to DataFrames and standardize column names
    gsm_df = pd.DataFrame(gsm_data)
    gsm_df = gsm_df.rename(columns={'input': 'question'})
    gsm_df['question_type'] = 'Code Execution'  # Add question type
    
    web_df = pd.DataFrame(web_data)
    web_df['question_type'] = 'Search Engine'  # Add question type
    
    # Combine datasets with matching column names
    combined_df = pd.concat([gsm_df, web_df]).reset_index(drop=True)
    
    # Initialize prediction column
    combined_df['question_type_prediction'] = None
    
    # Shuffle the combined dataset and limit to first 300 entries from each type
    combined_df = combined_df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # Get first 300 of each type
    code_execution_df = combined_df[combined_df['question_type'] == 'Code Execution'].head(300)
    search_engine_df = combined_df[combined_df['question_type'] == 'Search Engine'].head(300)
    
    # Combine and shuffle again
    combined_df = pd.concat([code_execution_df, search_engine_df])
    combined_df = combined_df.sample(frac=1, random_state=42).reset_index(drop=True)

    return combined_df

async def main():
    # Load datasets
    combined_df = combine_datasets()
    
    # Load tool examples
    tool_examples = load_tool_examples()
    
    # Process each question
    for idx, row in combined_df.iterrows():
        # Combine tool examples with current question
        prompt = f"{tool_examples}\n\nQuestion: {row['question']}\nAnswer:"
        
        # Call LLM with the prompt (now with await)
        response = await call_llm(prompt)
        
        # Store the response in the dataframe
        combined_df.at[idx, 'question_type_prediction'] = response
        
        # Print progress
        print(f"Question {idx + 1}/{len(combined_df)}:")
        print(f"True Type: {row['question_type']}")
        print(f"Predicted Type: {response}\n")

if __name__ == "__main__":
    asyncio.run(main())
