import json
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from chat.pipeline import chat_pipeline

from .forms import MessageForm
from .models import Message

schema = {
    "Complaint": {
        "fields": {
            "id": "integer",
            "description": "string",
            "sub_date": "datetime",
            "last_update_date": "datetime",
        },
        "relations": {
            "customer_account_ref": "User",
            "assigned_agent_ref": "User",
            "complaint_category_ref": "ComplaintCategory",
            "complaint_status_ref": "ComplaintStatus",
            "notes": "ManyToMany -> Notes"
        }
    },
    "ComplaintStatus": {
        "fields": {
            "id": "integer",
            "name": "string"
        }
    },
    "ComplaintCategory": {
        "fields": {
            "id": "integer",
            "name": "string"
        }
    },
    "Notes": {
        "fields": {
            "id": "integer",
            "description": "string",
            "last_update_date": "datetime"
        },
        "relations": {
            "user_ref": "User"
        }
    },
    "User": {
        "fields": {
            "id": "integer",
            "username": "string",
            "email": "string"
        },
        "relations": {
            "userprofile": "UserProfile"
        }
    },
    "UserProfile": {
        "fields": {
            "id": "integer",
            "service_plan_ref": "string"
        }
    },
    "ServicePlan": {
        "fields": {
            "id": "integer",
            "name": "string",
            "data": "float",
            "calls": "float",
            "sms": "integer"
        }
    }
}

schema_json = json.dumps(schema, indent=2)

@login_required
def ask_question_view(request):
    if request.method == "POST":
        form = MessageForm(request.POST)

        if form.is_valid():
            question = form.save(commit=False)
            question.user_ref = request.user

            response = chat_pipeline(request.user, question.prompt)

            question.response = response
            question.save()
            return redirect("ask_question")  # IMPORTANT

    else:
        form = MessageForm()

    messages = Message.objects.filter(user_ref=request.user).order_by("id")
    
    return render(request, "chat/index.html", {
        "form": form,
        "messages": messages,
    })