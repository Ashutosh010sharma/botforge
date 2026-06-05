from .models import BotKnowledge,WebsiteChunk
from .utils import create_chunks
from demo.gemini_service import generate_embedding


def process_knowledge(knowledge):

    WebsiteChunk.objects.filter(

        chatbot=knowledge.chatbot,

        source_type="knowledge",

        title=knowledge.title

    ).delete()


    chunks=create_chunks(

        knowledge.content
    )


    chunk_objects=[]


    for chunk in chunks:

        embedding=generate_embedding(
            chunk
        )

        chunk_objects.append(

            WebsiteChunk(

                chatbot=knowledge.chatbot,

                source_type="knowledge",
                source_id=knowledge.id,

                title=knowledge.title,

                chunk_text=chunk,

                embedding=embedding
            )
        )


    WebsiteChunk.objects.bulk_create(
        chunk_objects
    )


    print(
        f"{len(chunk_objects)} knowledge chunks created"
    )