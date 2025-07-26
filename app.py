from main import run_full_interview
import asyncio
from dotenv import load_dotenv
import fitz
load_dotenv()


if __name__=="__main__":
    final=asyncio.run(run_full_interview())
