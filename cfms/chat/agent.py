import os

from langchain_core.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from .tools import make_tools
from langchain.agents import create_tool_calling_agent

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")  # ✅ correct env var
)

def get_agent(user):
    tools = make_tools(user)

    prompt = ChatPromptTemplate.from_messages([
        ("system", """
You are a telecom assistant.

Rules:
- Always use tools for account-specific questions
- Never guess user data
- If data is unavailable, say so clearly
"""),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ])

    agent = create_tool_calling_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )

    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True
    )