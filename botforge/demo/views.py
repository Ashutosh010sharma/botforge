from django.shortcuts import render
from django.http import JsonResponse
from .models import SchoolKnowledge
from .search_service import find_best_chunks

from .gemini_service import generate_response


def school_demo_bot(request):

    return render(
        request,
        'demo/school_bot.html'
    )


def school_chat_api_bck(request):

    message = request.GET.get(
        'message',
        ''
    ).lower()


    responses={

        "admission":
        "School admissions are open from April to June.",

        "fees":
        "Annual school fees are ₹50,000.",

        "timing":
        "School timing is 8:00 AM to 2:00 PM.",

        "contact":
        "Contact us at +91-9876543210.",

        "principal":
        "Principal: Dr. Sharma"
    }


    reply=(
        "I couldn't understand your question."
    )

    for key,value in responses.items():

        if key in message:

            reply=value
            break


    return JsonResponse(
        {
            "response":reply
        }
    )
    
def school_chat_api_bcp12(request):

    try:

        message = request.GET.get(
            "message",
            ""
        ).lower()

        knowledge = SchoolKnowledge.objects.filter(
            title__icontains=message
        ).first()

        if knowledge:

            response = knowledge.content

        else:

            response = (
                "Sorry, I couldn't find information."
            )

        return JsonResponse({

            "response":response

        })

    except Exception as e:

        return JsonResponse({

            "response":str(e)

        })
    
    
    
def school_chat_api(request):

    try:

        message=request.GET.get(

            "message",
            ""
        )


        results=find_best_chunks(
            message
        )


        context="\n".join(

            [

                item["chunk"].chunk_text

                for item in results
            ]
        )


        response=generate_response(

            message,

            context
        )


        return JsonResponse({

            "response":response
        })


    except Exception as e:

        return JsonResponse({

            "response":str(e)
        })