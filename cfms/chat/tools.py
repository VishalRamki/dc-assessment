from langchain.tools import tool
from . import helpers


def make_tools(user):

    @tool
    def get_current_plan_tool():
        """Get the user's current service plan."""
        plan = helpers.get_current_plan(user)

        if not plan:
            return "No active service plan found."

        return (
            f"You are on the {plan['name']} plan. "
            f"It includes {plan['data_limit']}GB data, "
            f"{plan['call_limit']} call minutes, "
            f"and {plan['sms_limit']} SMS."
        )


    @tool
    def get_data_usage_tool():
        """Get the user's current usage."""
        usage = helpers.get_data_usage(user)

        if not usage:
            return "No usage data found."

        return (
            f"You have used {usage['data_used']}GB of data, "
            f"{usage['call_used']} call minutes, "
            f"and {usage['sms_used']} SMS."
        )


    @tool
    def get_open_complaints_tool():
        """Get user's open complaints."""
        complaints = helpers.get_open_complaints(user)

        if not complaints:
            return "You have no open complaints."

        return complaints


    @tool
    def get_last_payment_tool():
        """Get the user's most recent payment."""
        return helpers.get_last_payment(user)


    @tool
    def get_account_balance_tool():
        """Get the user's account balance."""
        return helpers.get_account_balance(user)


    @tool
    def get_outages_tool():
        """Check outages in user's area."""
        outages = helpers.get_outages(user)

        if not outages:
            return "No outages reported in your area."

        return outages


    return [
        get_current_plan_tool,
        get_data_usage_tool,
        get_open_complaints_tool,
        get_last_payment_tool,
        get_account_balance_tool,
        get_outages_tool,
    ]