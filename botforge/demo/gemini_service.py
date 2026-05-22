from google import genai

from django.conf import settings
import time


client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)

def generate_embedding(text):

    try:

        result = client.models.embed_content(

            model="gemini-embedding-001",

            contents=text
        )

        return result.embeddings[0].values

    except Exception as e:

        print(
            "Embedding Error:",
            str(e)
        )

        return None
    
def generate_response(question,context):
    try:
        prompt = f"""
        You are a friendly AI School Assistant.

        Rules:

        1. Answer naturally and conversationally.
        2. Use only the provided context.
        3. Keep answers concise unless details are requested.
        4. If user says "hi", "hello", "hey", greet them.
        5. If information is missing, say:
        "I couldn't find that information."
        6. Do not invent facts.
        7. Behave like a helpful school receptionist.

        Context:
        {context}

        User Question:
        {question}

        Answer:
        """

        max_retries = 3

        for attempt in range(max_retries):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    contents=prompt
                )
                return response.text
            except Exception as e:
                error = str(e)
                print(
                    f"Gemini Attempt {attempt+1}: {error}"
                    )


                if "503" in error:
                    time.sleep(2)
                    continue
                else:
                    raise e


        return ("The AI assistant is currently busy. "
                "Please try again in a few seconds.")


    except Exception as e:
        print(
            "Response Error:",
            str(e)

        )

        return ("Sorry, I couldn't process your request right now.")