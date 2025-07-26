import os
import json
import asyncio
from dotenv import load_dotenv
from google import genai

load_dotenv()
client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-1.5-flash"

# ---------- Question Generation ----------

def clean_output(response_text:str)->list:
    if(response_text.startswith("```json")): 
        response_text=response_text.strip("`").strip("json").strip()
    
    if(response_text.endswith("```")): 
        response_text=response_text.strip("`").strip()

    return response_text
def generate_questions(role: str, description: str, count: int,level:int) -> list[str]:
    prompt = f"""
Generate {count} interview questions which are of {level} level. And these questions should cover all important
and fundamental concepts which is present in {description}. By learning from these questions, user should get a good amount of 
knowledge about those concepts.
Return only a JSON array of questions. Example:
[
  "Question 1?",
  "Question 2?",
  ...
]
"""
    
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )
    res=clean_output(response.text)
    print("response: ",res)
    return json.loads(res)

