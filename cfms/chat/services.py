from .services_llm import classify_intents_llm, extract_filters

from . import helpers


def classify_intent(query: str):
    q = query.lower()

    if "plan" in q:
        return "plan"
    elif "balance" in q:
        return "balance"
    elif "data" in q or "usage" in q:
        return "usage"
    elif "complaint" in q:
        return "complaints"
    elif "payment" in q:
        return "payment"
    elif "outage" in q or "fault" in q:
        return "outage"

    return "unknown"


def handle_query(user, query: str):
    intents = classify_intents_llm(query)
    filters = extract_filters(query)


    results = {}

    for intent in intents:
        if intent == "plan":
            results["plan"] = helpers.get_current_plan(user)

        elif intent == "usage":
            results["usage"] = helpers.get_data_usage(user)

        elif intent == "complaints":
            results["complaints"] = helpers.get_open_complaints(user, filters=filters)

        elif intent == "payment":
            results["payment"] = helpers.get_last_payment(user)

        elif intent == "balance":
            results["balance"] = helpers.get_account_balance(user)

        elif intent == "outage":
            results["outage"] = helpers.get_outages(user)

    return results