from django.shortcuts import render
from django.http import JsonResponse


def school_demo_bot(request):

    return render(
        request,
        'demo/school_bot.html'
    )


def school_chat_api(request):

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