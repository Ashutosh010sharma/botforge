from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import (Chatbot)
from django.http import JsonResponse
from django.db import transaction

# Create your views here.
@login_required
def bot_list(request):

    bots = Chatbot.objects.filter(

        company=request.user.company

    ).order_by("-created_at")

    return render(request,"bots/list.html",{"bots": bots}
    )


@login_required
@login_required
def bot_create(request):

    try:

        if request.method == "POST":

            with transaction.atomic():

                Chatbot.objects.create(

                    company=request.user.company,

                    name=request.POST.get(
                        "name"
                    ),

                    bot_type=request.POST.get(
                        "bot_type"
                    ),

                    description=request.POST.get(
                        "description"
                    ),

                    welcome_message=request.POST.get(
                        "welcome_message"
                    )
                )

            return JsonResponse({

                "status": True,

                "message":
                "Bot created successfully."
            })

        return render(

            request,

            "bots/create.html"
        )

    except Exception as e:

        return JsonResponse({

            "status": False,

            "message": str(e)
        }, status=400)
