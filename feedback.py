import json
from google import genai
import os
from tech import clean_output

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-1.5-flash"  # newer, recommended version


def clean_output(response_text:str)->list:
    if(response_text.startswith("```json")): 
        response_text=response_text.strip("`").strip("json").strip()
    
    if(response_text.endswith("```")): 
        response_text=response_text.strip("`").strip()

    return response_text
async def rate_answer(question: str, answer: str) -> dict:
    prompt = f"""
You are an expert technical interviewer evaluating candidate responses.

Question: {question}
Answer: {answer}

Evaluate the answer based on:
1. **Clarity** – Is the explanation understandable and logically structured?
2. **Relevance** – Does it directly answer the question?
3. **Depth** – Does it reflect deeper understanding, with examples or elaboration?

Follow this step-by-step reasoning:
- Identify if all key concepts required by the question are covered.
- Note any missing important concepts.
- Assess if the answer is vague, partially correct, or well-articulated.
- Use the rubric below to decide the score:

### Scoring Rubric:
- **5** – Fully correct, clear, well-structured, includes examples or deeper insight.
- **4** – Mostly correct, a few missing points but overall good.
- **3** – Adequate understanding but lacks detail or clarity.
- **2** – Incomplete, fundamental ideas are missing.
- **1** – Incorrect or uninformative (e.g., “I don’t know”,""I am learning"", or off-topic).

### Example:
Q: Explain pass-by-value vs pass-by-reference.
A: Pass by value copies the variable; pass by reference uses the actual variable.
Rating: 3
Feedback: Good understanding shown, but could use examples from specific languages.

Q: Explain the concept of Polymorphism and Inheritance in java
A: Polymorphism is basically having many types or ways of denotation of one thing example we can have more than one constructor of a class to show that in different ways
Rating: 3
Feedback: User did not given answer of both the terms asked, lacks understanding.
---
***These are just examples showcasing how to react don't copy them everywhere.***


Now rate the candidate's answer following the rubric above.

Reply ONLY with a **valid JSON object** in the following format:
{{
  "rating": <1-5>,
  "feedback": "<1-sentence constructive feedback>"
}}
"""


    resp = client.models.generate_content(
        model=MODEL,
        contents=prompt,
    )

    try:
        res=clean_output(resp.text)

        j=json.loads(res)
        
        return {"rating": int(j["rating"]), "feedback": j["feedback"]}
    except Exception:
        return {"rating": 3, "feedback": "Unable to parse—default neutral rating."}


# ---------- Interview Stage ----------
async def conduct_stage(stage_name: str, questions: list,final_eval:list, pass_threshold=0.6) -> dict:
    print(f"\n🚀 Starting {stage_name} Round...\n")
    good, total = 0, 0

    
    for idx, question in enumerate(questions):
        print(f"\nQ{idx+1}: {question}")
        ans = input("Your Answer: ")
        eval = await rate_answer(question, ans)
        final_eval.append({
            "Question No":{idx+1},
            "rating":eval["rating"],
            "feedback":eval["feedback"],
        })
        good += (eval["rating"] >= 3)
        total += 1

        

    success = (good / total) >= pass_threshold
    print(f"\n✅ {stage_name} Round Completed. Score: {good}/{total}")
    return {
        "result":success,
        "final_report":final_eval
    }

