from .search_service import find_best_chunks
from demo.gemini_service import generate_response


def ask_bot(chatbot,question):
    #print(chatbot)

    active_knowledge=chatbot.knowledge_items.filter(
        is_deleted=False
    ).count()

    active_pages=chatbot.pages.filter(
        is_deleted=False
    ).count()
    # print("Active Pages:", chatbot.pages.filter(
    # is_deleted=False
    # ).count())

    # print("Active Knowledge:", chatbot.knowledge_items.filter(
    #     is_deleted=False
    # ).count())

    total_knowledge=chatbot.knowledge_items.count()

    if active_knowledge==0 and active_pages==0:

        if total_knowledge==0:

            return (
                "This chatbot does not have any knowledge configured yet. "
                "Please add website pages or knowledge content first."
            )

        return (
            "The knowledge base for this chatbot has been removed or is currently unavailable."
        )

    results=find_best_chunks(
        chatbot,
        question
    )

    if not results:

        return (
            "I could not find any relevant information related to your question "
            "in the available knowledge base."
        )

    context="\n\n".join(

        [

            f"Source: {item['chunk'].title}\n\n{item['chunk'].chunk_text}"

            for item in results

        ]

    )

    response=generate_response(
        question,
        context,
        chatbot
    )

    return response