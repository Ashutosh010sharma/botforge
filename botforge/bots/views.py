from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Chatbot,BotKnowledge,WebsiteChunk,ChatSession,ChatMessage
from django.http import JsonResponse
from django.db import transaction
from .crawl_service import crawl_and_save

from .training_service import train_chatbot
from .knowledge_service import process_knowledge
from .chat_service import ask_bot
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from django.db.models.functions import TruncDate
from datetime import timedelta
from django.utils import timezone
import json
from accounts.models import Company
from billing.models import Subscription


# Create your views here.
@login_required
def bot_list(request):

    company = Company.objects.filter(
        user=request.user,
    ).first()


    bots = Chatbot.objects.filter(

        company=company,
        is_deleted=False

    ).order_by("-created_at")

    return render(

        request,
        "bots/list.html",

        {
            "bots": bots
        }

    )


def bot_create(request):

    try:

        company = Company.objects.filter(
            user=request.user,
            is_active=True
        ).first()

        if not company:

           return JsonResponse({

                "status": False,

                "code": "COMPANY_REQUIRED",

                "message":
                "Please setup your company before creating a bot."

            })

        subscription = Subscription.objects.filter(

            company=company,

            is_active=True

        ).select_related(
            "plan"
        ).first()

        if not subscription:

           return JsonResponse({

                "status": False,

                "code": "PLAN_REQUIRED",

                "message":
                "Please select a plan before creating a bot."

            })

        current_bots = Chatbot.objects.filter(

            company=company,

            is_deleted=False

        ).count()

        if current_bots >= subscription.plan.max_bots:

           return JsonResponse({

                "status": False,

                "code": "BOT_LIMIT",

                "message":
                f"Your {subscription.plan.name} plan allows only "
                f"{subscription.plan.max_bots} bot(s). Please upgrade your plan."

            })

        if request.method == "POST":

            with transaction.atomic():

                Chatbot.objects.create(

                    company=company,

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

    bot=get_object_or_404(
        Chatbot,
        id=bot_id,
        company__user=request.user,
        is_deleted=False
    )

    pages=bot.pages.filter(is_deleted=False)

    pages_count=pages.count()

    chunks_count=WebsiteChunk.objects.filter( chatbot=bot,is_deleted=False).count()

    conversations=bot.chat_sessions.filter(
        is_deleted=False
    )

    conversations_count=conversations.count()

    messages_count=ChatMessage.objects.filter(
        session__chatbot=bot,
        session__is_deleted=False
    ).count()
    
    last_7_days=timezone.now()-timedelta(days=6)

    conversation_stats=(
        ChatSession.objects.filter(
            chatbot=bot,
            is_deleted=False,
            created_at__gte=last_7_days
        )
        .annotate(day=TruncDate("created_at"))
        .values("day")
        .annotate(total=Count("id"))
        .order_by("day")
    )

    conversation_categories=[]
    conversation_data=[]

    for item in conversation_stats:

        conversation_categories.append(
            item["day"].strftime("%d %b")
        )

        conversation_data.append(
            item["total"]
        )


    message_stats=(
        ChatMessage.objects.filter(
            session__chatbot=bot,
            session__is_deleted=False,
            created_at__gte=last_7_days
        )
        .annotate(day=TruncDate("created_at"))
        .values("day")
        .annotate(total=Count("id"))
        .order_by("day")
    )

    message_categories=[]
    message_data=[]

    for item in message_stats:

        message_categories.append(
            item["day"].strftime("%d %b")
        )

        message_data.append(
            item["total"]
        )

    context={

        "bot":bot,

        "pages_count":pages_count,

        "chunks_count":chunks_count,

        "knowledge_count":bot.knowledge_items.filter(
            is_deleted=False
        ).count(),

        "conversations_count":conversations_count,

        "messages_count":messages_count,

        "visitors_count":conversations_count,

        "widget_installs":1 if bot.is_installed else 0,

        "recent_pages":pages.order_by("-id"),

        "knowledge_items":bot.knowledge_items.filter(
            is_deleted=False
        ).order_by("-id"),

        "sessions":conversations.order_by(
            "-updated_at"
        ),
        "conversation_chart_categories":json.dumps(
            conversation_categories
        ),

        "conversation_chart_data":json.dumps(
            conversation_data
        ),

        "message_chart_categories":json.dumps(
            message_categories
        ),

        "message_chart_data":json.dumps(
            message_data
        ),

    }

    return render(

        request,

        "bots/workspace.html",

        context

    )
@login_required
def train_bot(request,bot_id):

    try:
        bot = get_object_or_404(Chatbot,id=bot_id,company__user=request.user,is_deleted=False)

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

        session_id=data.get(
            "session_id"
        )

        session,_=ChatSession.objects.get_or_create(

            chatbot=bot,

            session_id=session_id

        )

        ChatMessage.objects.create(

            session=session,

            sender="user",

            message=message

        )

        response=ask_bot(

            bot,

            message

        )

        ChatMessage.objects.create(

            session=session,

            sender="bot",

            message=response

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


def widget_config(request,widget_key):

    bot=get_object_or_404(
        Chatbot,
        widget_key=widget_key,
        is_active=True
    )

    return JsonResponse({

        "success":True,

        "name":bot.name,

        "welcome_message":bot.welcome_message,

        "color":bot.theme_color,

        "position":bot.widget_position

    })
    
@login_required
def conversation_detail_ajax(request,session_id):

    session=get_object_or_404(
        ChatSession,
        id=session_id
    )

    messages=session.messages.all().order_by(
        "created_at"
    )

    data=[]

    for msg in messages:

        data.append({

            "sender":msg.sender,

            "message":msg.message,

            "time":timezone.localtime(msg.created_at).strftime("%d %b %Y %I:%M %p")

        })

    return JsonResponse({

        "success":True,

        "messages":data

    })
    

@login_required
def clear_chat_history(request,bot_id):

    bot=get_object_or_404(
        Chatbot,
        id=bot_id,
        company__user=request.user
    )

    ChatSession.objects.filter(
        chatbot=bot,
        is_deleted=False
    ).update(

        is_deleted=True,

        deleted_at=timezone.now()

    )

    return JsonResponse({

        "success":True,

        "message":"Chat history moved to trash."

    })
    
@login_required
def delete_knowledge_base(request,bot_id):

    bot=get_object_or_404(
        Chatbot,
        id=bot_id,
        company__user=request.user
    )

    bot.knowledge_items.filter(
        is_deleted=False
    ).update(

        is_deleted=True,

        deleted_at=timezone.now()

    )

    bot.pages.filter(
        is_deleted=False
    ).update(

        is_deleted=True,

        deleted_at=timezone.now()

    )

    WebsiteChunk.objects.filter(
        chatbot=bot,
        is_deleted=False
    ).update(

        is_deleted=True,

        deleted_at=timezone.now()

    )

    return JsonResponse({

        "success":True,

        "message":"Knowledge base moved to trash."

    })
    
@login_required
def delete_chatbot(request,bot_id):

    bot=get_object_or_404(
        Chatbot,
        id=bot_id,
        company__user=request.user
    )

    bot.is_deleted=True

    bot.deleted_at=timezone.now()

    bot.save()

    return JsonResponse({

        "success":True,

        "message":"Chatbot moved to trash."

    })
    
def documention(request):
    return render(request, "bots/documentation.html")
    