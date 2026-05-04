from .services_llm import format_with_groq
from .services import handle_query

def chat_pipeline(user, query: str):
    data = handle_query(user, query)

    friendly_response = format_with_groq(query, data)

    return friendly_response