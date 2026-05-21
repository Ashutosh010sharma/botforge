def create_chunks(
    text,
    chunk_size=300
):

    chunks=[]

    start=0


    while start < len(text):

        end=start+chunk_size

        chunks.append(

            text[start:end]

        )

        start=end


    return chunks