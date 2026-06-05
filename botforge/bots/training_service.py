from .models import WebsiteChunk
from .utils import create_chunks
from demo.gemini_service import generate_embedding


def create_page_chunks(page):

    page.chunks.all().delete()

    chunks = create_chunks(
        page.content
    )

    chunk_objects = []

    for chunk in chunks:

        chunk_objects.append(

            WebsiteChunk(

                chatbot=page.chatbot,

                page=page,

                source_type="website",
                source_id=page.id,

                title=page.title,

                chunk_text=chunk
            )
        )

    WebsiteChunk.objects.bulk_create(
        chunk_objects
    )

    print(
        f"{len(chunk_objects)} chunks created"
    )
    



def generate_chunk_embeddings(chatbot):

    chunks = chatbot.chunks.all()

    for chunk in chunks:

        if chunk.embedding:

            continue

        print(
            f"Embedding Chunk {chunk.id}"
        )

        embedding = generate_embedding(
            chunk.chunk_text
        )

        if embedding:

            chunk.embedding = embedding

            chunk.save(
                update_fields=["embedding"]
            )

    print(
        "Embeddings Generated"
    )
    
def train_chatbot(chatbot):

    chatbot.status = "training"

    chatbot.save()

    for page in chatbot.pages.all():

        create_page_chunks(
            page
        )

    generate_chunk_embeddings(
        chatbot
    )

    chatbot.status = "active"

    chatbot.save()

    print(
        "Bot Training Complete"
    )