from django.utils import timezone
from django.db.models import Sum
from dashboard.models import Complaint, UserProfile


def get_user_profile(user):
    try:
        return UserProfile.objects.select_related(
            "service_plan_ref", "area_ref"
        ).get(user=user)
    except UserProfile.DoesNotExist:
        return None


def get_current_plan(user):
    profile = get_user_profile(user)
    if not profile or not profile.service_plan_ref:
        return None

    plan = profile.service_plan_ref
    return {
        "name": plan.name,
        "data_limit": plan.data,
        "call_limit": plan.call,
        "sms_limit": plan.sms,
    }


def get_data_usage(user):
    profile = get_user_profile(user)
    if not profile:
        return None

    return {
        "data_used": profile.data,
        "call_used": profile.call,
        "sms_used": profile.sms,
    }


def get_open_complaints(user):
    complaints = Complaint.objects.select_related(
        "complaint_status_ref",
        "complaint_category_ref"
    ).filter(
        customer_account_ref=user,
        complaint_status_ref__name__iexact="open"
    )

    return [
        {
            "id": c.id,
            "description": c.description,
            "category": c.complaint_category_ref.name,
            "status": c.complaint_status_ref.name,
            "submitted": c.sub_date,
        }
        for c in complaints
    ]


def get_last_payment(user):
    """
    You don't have a Payment model yet.
    """
    return "Payment system not implemented yet."


def get_account_balance(user):
    """
    No billing model exists.
    """
    return "Billing system not implemented yet."


def get_outages(user):
    profile = get_user_profile(user)
    if not profile or not profile.area_ref:
        return []

    # No outage model exists
    return "Outage system not implemented yet."