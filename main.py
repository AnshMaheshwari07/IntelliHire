import asyncio
import os

from tech import generate_questions
from feedback import conduct_stage


# ---------- Main Flow ----------



async def run_full_interview():
    role = "Software Engineer"
    tech_qs = generate_questions(role, "Should have good understanding of python,c++,java", 1,"easy")

    # Stage 1: Technical
    final_eval=[]
    passed_tech = await conduct_stage("Technical", tech_qs,final_eval)
    
    if not passed_tech["result"]:
        print("Final_report: \n",final_eval)
        print("\n❌ Candidate rejected after technical round.")
        return
    hr_qs = generate_questions(role, "should have some good analytical and behavioral/situational skills", 1,"medium")


    # Stage 2: HR
    passed_hr = await conduct_stage("HR", hr_qs,final_eval)

    if passed_hr["result"]:
        print("\n🎉 Candidate PASSED both rounds! Offer recommended.")
        print("Final_report: \n",final_eval)
    else:
        print("\n🤝 Candidate failed HR round. Consider for future.")
        print("Final_report: \n",final_eval)


