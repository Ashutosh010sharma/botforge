from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Chatbot,BotKnowledge,WebsiteChunk
from django.http import JsonResponse
from django.db import transaction
from .crawl_service import crawl_and_save

from .training_service import train_chatbot
from .knowledge_service import process_knowledge
from django.utils import timezone
from .chat_service import ask_bot
from django.views.decorators.csrf import csrf_exempt
import json


# Create your views here.
@login_required
def bot_list(request):

    bots = Chatbot.objects.filter(

        company=request.user.company

    ).order_by("-created_at")

    return render(request,"bots/list.html",{"bots": bots}
    )


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
                     website_url=request.POST.get(
                        "website_url"
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
        
@login_required
def bot_workspace(request,bot_id):

    bot = get_object_or_404(Chatbot,id=bot_id,company__user=request.user)

    pages_count = bot.pages.count()

    chunks_count = sum(

        page.chunks.count()

        for page in bot.pages.all()
    )

    context = {

        "bot": bot,

        "pages_count": pages_count,

        "chunks_count": chunks_count,

        "knowledge_count": 0,

        "conversations_count": 0,

        "visitors_count": 0,

        "widget_installs": 0,

        "recent_pages": bot.pages.all().order_by("-id"),
        "knowledge_items": bot.knowledge_items.filter(is_deleted=False).order_by("-id")
    }

    return render(

        request,

        "bots/workspace.html",

        context
    )
    
@login_required
def train_bot(request,bot_id):

    try:
        bot = get_object_or_404(Chatbot,id=bot_id,company__user=request.user)

        bot.status = "training"

        bot.save()

        crawl_and_save(bot)

        train_chatbot(bot)

        bot.status = "active"

        bot.save()

        return JsonResponse({

            "success":True,

            "message":"Bot trained successfully"
        })

    except Exception as e:

        return JsonResponse({

            "success":False,

            "message":str(e)
        })
        
@login_required
def recrawl_bot(
    request,
    bot_id
):

    try:

        bot = get_object_or_404(

            Chatbot,

            id=bot_id,

            company__user=request.user
        )

        bot.status = "training"

        bot.save()

        bot.pages.all().delete()

        crawl_and_save(
            bot
        )

        train_chatbot(
            bot
        )

        bot.status = "active"

        bot.save()

        return JsonResponse({

            "success":True,

            "message":"Website re-crawled successfully."
        })

    except Exception as e:

        return JsonResponse({

            "success":False,

            "message":str(e)
        })
        
        
@login_required
def add_knowledge(request,bot_id):

    try:

        bot=get_object_or_404(

            Chatbot,

            id=bot_id,

            company__user=request.user
        )


        title=request.POST.get(
            "title"
        )

        content=request.POST.get(
            "content"
        )


        knowledge=BotKnowledge.objects.create(

            chatbot=bot,

            title=title,

            content=content
        )


        process_knowledge(
            knowledge
        )


        return JsonResponse({

            "success":True,

            "message":"Knowledge added successfully"
        })


    except Exception as e:

        return JsonResponse({

            "success":False,

            "message":str(e)
        })
        
@login_required
def delete_knowledge(request,id):

    try:

        knowledge=get_object_or_404(

            BotKnowledge,

            id=id,

            chatbot__company__user=request.user
        )

        knowledge.is_deleted=True

        knowledge.deleted_at=timezone.now()

        knowledge.save(

            update_fields=[
                "is_deleted",
                "deleted_at"
            ]
        )

        WebsiteChunk.objects.filter(

            chatbot=knowledge.chatbot,

            source_type="knowledge",

            title=knowledge.title,
            source_id=knowledge.id

        ).delete()

        return JsonResponse({

            "success":True,

            "message":"Knowledge moved to trash."
        })

    except Exception as e:

        return JsonResponse({

            "success":False,

            "message":str(e)
        })
        
@login_required
def update_knowledge(request,id):

    try:

        knowledge=get_object_or_404(
            BotKnowledge,
            id=id,
            chatbot__company__user=request.user
        )

        old_title=knowledge.title

        knowledge.title=request.POST.get("title")
        knowledge.content=request.POST.get("content")
        knowledge.save()

        WebsiteChunk.objects.filter(
            chatbot=knowledge.chatbot,
            source_type="knowledge",
            title=old_title
        ).delete()

        process_knowledge(
            knowledge
        )

        return JsonResponse({
            "success":True,
            "message":"Knowledge updated successfully."
        })

    except Exception as e:

        return JsonResponse({
            "success":False,
            "message":str(e)
        })
        
@login_required
def test_chat_api(request,bot_id):

    try:

        bot=get_object_or_404(
            Chatbot,
            id=bot_id,
            company__user=request.user
        )

        message=request.GET.get(
            "message",
            ""
        )

        response=ask_bot(
            bot,
            message
        )

        return JsonResponse({

            "success":True,

            "response":response
        })

    except Exception as e:

        return JsonResponse({

            "success":False,

            "response":str(e)
        })
        
@login_required
def save_widget_settings(request,bot_id):

    try:

        bot=get_object_or_404(
            Chatbot,
            id=bot_id,
            company__user=request.user
        )

        bot.theme_color=request.POST.get(
            "theme_color"
        )

        bot.widget_position=request.POST.get(
            "widget_position"
        )

        bot.welcome_message=request.POST.get(
            "welcome_message"
        )

        bot.save()

        return JsonResponse({

            "success":True,

            "message":"Widget settings saved successfully."

        })

    except Exception as e:

        return JsonResponse({

            "success":False,

            "message":str(e)

        })
        
@login_required
def install_bot(request,bot_id):

    try:

        bot=get_object_or_404(
            Chatbot,
            id=bot_id,
            company__user=request.user
        )

        bot.is_installed=True
        bot.installed_at=timezone.now()

        bot.save()

        return JsonResponse({

            "success":True,

            "message":"Chatbot installed successfully.",

            "widget_key":str(
                bot.widget_key
            )

        })

    except Exception as e:

        return JsonResponse({

            "success":False,

            "message":str(e)

        })
        
@csrf_exempt
def widget_chat_api(request,widget_key):

    try:

        bot=get_object_or_404(

            Chatbot,

            widget_key=widget_key,

            is_installed=True,

            is_active=True

        )

        data=json.loads(
            request.body
        )

        message=data.get(
            "message",
            ""
        )

        response=ask_bot(
            bot,
            message
        )

        return JsonResponse({

            "success":True,

            "response":response

        })

    except Exception as e:

        return JsonResponse({

            "success":False,

            "response":str(e)

        })
