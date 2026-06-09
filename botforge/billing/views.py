from django.shortcuts import render

# Create your views here.
from .models import Plan
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from accounts.models import Company
from bots.models import Chatbot,WebsitePage,ChatMessage



def pricing(request):

    plans = Plan.objects.filter(
        is_active=True
    ).order_by(
        "monthly_price"
    )

    subscription = None

    if request.user.is_authenticated:

        company = Company.objects.filter(
            user=request.user
        ).first()

        if company:

            subscription = Subscription.objects.filter(
                company=company,
                is_active=True
            ).select_related(
                "plan"
            ).first()

    return render(

        request,

        "billing/pricing.html",

        {

            "plans": plans,

            "subscription": subscription

        }

    )


def subscription(request):

    return render(

        request,

        "billing/subscription.html"
    )
    
from billing.models import (
    Plan,
    Subscription
)


@login_required
def select_plan(request):

    try:

        if request.method != "POST":

            return JsonResponse({

                "status": False,

                "message": "Invalid request."

            })

        plan_id = request.POST.get(
            "plan_id"
        )

        plan = Plan.objects.filter(

            id=plan_id,

            is_active=True

        ).first()

        if not plan:

            return JsonResponse({

                "status": False,

                "message": "Selected plan not found."

            })

        company = Company.objects.filter(

            user=request.user,

            is_active=True

        ).first()

        if not company:

            return JsonResponse({

                "status": False,

                "code": "COMPANY_REQUIRED",

                "message":
                "Please setup your company first."

            })

        subscription = Subscription.objects.filter(

            company=company,

            is_active=True

        ).select_related(
            "plan"
        ).first()

        # Already using this plan
        if (

            subscription and

            subscription.plan_id == plan.id

        ):

            return JsonResponse({

                "status": False,

                "code": "CURRENT_PLAN",

                "message":
                "You are already using this plan."

            })

        current_bots = Chatbot.objects.filter(

            company=company,

            is_deleted=False

        ).count()

        # Downgrade validation
        if current_bots > plan.max_bots:

            return JsonResponse({

                "status": False,

                "code": "DOWNGRADE_BLOCKED",

                "message":
                f"You currently have {current_bots} bots. "
                f"The selected plan allows only "
                f"{plan.max_bots} bots."

            })

        # Create subscription
        if not subscription:

            Subscription.objects.create(

                company=company,

                plan=plan,

                is_active=True

            )

        else:

            subscription.plan = plan

            subscription.save()

        return JsonResponse({

            "status": True,

            "message":
            f"{plan.name} plan activated successfully."

        })

    except Exception as e:

        return JsonResponse({

            "status": False,

            "message": str(e)

        })
        
@login_required
def billing_dashboard(request):

    company = Company.objects.filter(
        user=request.user,
        is_active=True
    ).first()

    if not company:

        messages.error(

            request,

            "Please setup your company first."

        )

        return redirect(
            "company_setup"
        )

    subscription = Subscription.objects.filter(

        company=company,

        is_active=True

    ).select_related(
        "plan"
    ).first()

    if not subscription:

        return redirect(
            "pricing"
        )

    bots_used = Chatbot.objects.filter(

        company=company,

        is_deleted=False

    ).count()

    pages_used = WebsitePage.objects.filter(

        chatbot__company=company,

        is_deleted=False

    ).count()

    messages_used = ChatMessage.objects.filter(

        session__chatbot__company=company,

        session__is_deleted=False

    ).count()
    bots_percentage = min(

    round(
        (bots_used /
        subscription.plan.max_bots) * 100
    ),

    100

    )

    pages_percentage = min(

        round(
            (pages_used /
            subscription.plan.max_pages) * 100
        ),

        100

    )

    messages_percentage = min(

        round(
            (messages_used /
            subscription.plan.max_messages) * 100
        ),

        100

    )
    bot_limit_reached = (
    bots_used >=
    subscription.plan.max_bots
    )

    page_limit_reached = (
        pages_used >=
        subscription.plan.max_pages
    )

    message_limit_reached = (
        messages_used >=
        subscription.plan.max_messages
    )

    context = {

        "subscription": subscription,

        "bots_used": bots_used,

        "pages_used": pages_used,

        "messages_used": messages_used,
        "bots_percentage": bots_percentage,

        "pages_percentage": pages_percentage,

        "messages_percentage": messages_percentage,
        "bot_limit_reached": bot_limit_reached,
        "page_limit_reached": page_limit_reached,
        "message_limit_reached": message_limit_reached,

    }

    return render(

        request,

        "billing/dashboard.html",

        context

    )
