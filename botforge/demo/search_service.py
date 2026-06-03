import numpy as np

from .models import SchoolKnowledgeChunk
from .gemini_service import generate_embedding


def cosine_similarity(
    vector1,
    vector2
):

    vector1=np.array(vector1)

    vector2=np.array(vector2)

    similarity=np.dot(
        vector1,
        vector2
    ) / (

        np.linalg.norm(vector1)
        *
        np.linalg.norm(vector2)
    )

    return similarity


def find_best_chunks(

    question,

    chunk_model,

    top_k=3,

    min_score=0.60
):


    question_embedding=generate_embedding(

        question
    )


    results=[]


    chunks=chunk_model.objects.exclude(

        embedding__isnull=True
    )


    for chunk in chunks:

        score=cosine_similarity(

            question_embedding,

            chunk.embedding
        )


        if score >= min_score:

            results.append(

                {

                    "chunk":chunk,

                    "score":score
                }

            )


    results=sorted(

        results,

        key=lambda x:x["score"],

        reverse=True
    )


    return results[:top_k]