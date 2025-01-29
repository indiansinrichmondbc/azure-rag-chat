import openai

def embeddings(text):
    response = openai.Embedding.create(
        input=text,
        engine="text-embedding-ada-002"
    )
    return response['data'][0]['embedding']
