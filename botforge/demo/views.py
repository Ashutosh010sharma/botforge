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

    
    
def school_chat_api(request):

    try:

        message=request.GET.get(

            "message",
            ""
        )


        results=find_best_chunks(
            message
        )
        print("Test:",results)


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