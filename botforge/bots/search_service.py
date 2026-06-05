import math
from .models import WebsiteChunk
from demo.gemini_service import generate_embedding

def cosine_similarity(vec1,vec2):

    dot_product=sum(
        a*b for a,b in zip(vec1,vec2)
    )

    norm1=math.sqrt(
        sum(a*a for a in vec1)
    )

    norm2=math.sqrt(
        sum(b*b for b in vec2)
    )

    if norm1==0 or norm2==0:
        return 0

    return dot_product/(norm1*norm2)


def find_best_chunks(chatbot,question,top_k=5):

    query_embedding=generate_embedding(
        question
    )

    chunks=WebsiteChunk.objects.filter(
        chatbot=chatbot
    )

    results=[]

    for chunk in chunks:

        if not chunk.embedding:
            continue

        score=cosine_similarity(
            query_embedding,
            chunk.embedding
        )

        if score > 0.45:

            results.append({
                "chunk":chunk,
                "score":score
            })

    results.sort(
        key=lambda x:x["score"],
        reverse=True
    )

    return results[:top_k]