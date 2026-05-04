import os
import json
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage


llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)


INTENTS = [
    "plan",
    "balance",
    "usage",
    "complaints",
    "payment",
    "outage"
]

import json
from datetime import datetime

def safe_json(data):
    return json.dumps(
        data,
        default=lambda o: o.isoformat() if isinstance(o, datetime) else str(o)
    )

def classify_intents_llm(query: str):
    system_prompt = f"""
You are an intent classification system.

Available intents:
{INTENTS}

Rules:
- Return ONLY a JSON array
- Include ALL relevant intents
- If none match, return ["unknown"]
- No explanations

Examples:
Input: "What plan am I on?"
Output: ["plan"]

Input: "Check my balance and last payment"
Output: ["balance", "payment"]
"""

    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=query)
    ])

    content = response.content.strip()

    try:
        intents = json.loads(content)
        if isinstance(intents, list):
            return intents
    except Exception:
        pass

    return ["unknown"]

def format_with_groq(user_query: str, data: dict):
    system_prompt = """
You are a telecom assistant.

Your job:
- Convert structured JSON into a friendly, short response
- Do NOT invent data
- If a field is missing, ignore it
- Be concise and helpful
"""

    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"""
User question:
{user_query}

Data (JSON from backend):
{safe_json(data)}
""")
    ])

    return response.content