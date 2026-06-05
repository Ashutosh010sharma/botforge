from .search_service import find_best_chunks
from demo.gemini_service import generate_response


def ask_bot(chatbot,question):

    results=find_best_chunks(
        chatbot,
        question
    )

    if not results:

        return "I couldn't find relevant information in my knowledge base."

    context="\n\n".join(

        [

            f"Source: {item['chunk'].title}\n\n{item['chunk'].chunk_text}"

            for item in results

        ]

    )

    response=generate_response(
        question,
        context
    )

    return response