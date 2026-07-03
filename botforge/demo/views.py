from django.shortcuts import render
from django.http import JsonResponse
from .models import (SchoolKnowledgeChunk,HealthcareKnowledgeChunk,EcommerceKnowledgeChunk)
from .search_service import find_best_chunks

from .gemini_service import generate_response


def school_demo_bot(request):
    return render(request,'demo/school_bot.html')

    
        
def healthcare_demo_bot(request):
    return render(request,'demo/healthcare_bot.html')
def ecommerce_demo_bot(request):
    return render(request,'demo/ecommerce_bot.html')

def chatbot_api(request,bot_type):

    try:

        message=request.GET.get(

            "message",
            ""
        )


        model_mapping={

            "school":
            SchoolKnowledgeChunk,

            "healthcare":
            HealthcareKnowledgeChunk,

            "ecommerce":
            EcommerceKnowledgeChunk
        }


        chunk_model=model_mapping.get(

            bot_type
        )
        #print(bot_type)


        if not chunk_model:

            return JsonResponse({

                "response":
                "Invalid bot type."
            })


        results=find_best_chunks(

            question=message,

            chunk_model=chunk_model
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

            context,
            bot_type
        )


        return JsonResponse({

            "response":response
        })


    except Exception as e:

        return JsonResponse({

            "response":str(e)
        })
    