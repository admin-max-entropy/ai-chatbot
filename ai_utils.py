import openai
import config
import functools
from pinecone import Pinecone


openai.api_key = config.OPENAI_API_KEY

def get_openai_embedding(text: str, model="text-embedding-ada-002") -> list:
    response = openai.embeddings.create(input=text, model=model)
    return response.data[0].embedding

@functools.lru_cache()
def summarize_speech(speech_text):
    """
    Function to summarize a central bank speech using OpenAI API.
    """
    client = openai.OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4o",

        messages=[
            {"role": "system", "content": "You are an expert in Federal Reserve policies."},
            {"role": "user", "content": f"Summarize the following speech:\n\n{speech_text}"}
        ],

        functions=[
            {
                "name": "summarize_speech",
                "description": "Summarizes a speech into 3-5 key points.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "summaries": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "Title": {"type": "string"},
                                    "Description": {"type": "string"},
                                    "Source": {"type": "string"},
                                },
                                "required": ["Title", "Description", "Source"]
                            },
                            "description": "An array of key points summarizing the speech and the URL sources."
                        }
                    },
                    "required": ["summaries"]
                }
            }
        ],
        function_call={"name": "summarize_speech"}
    )
    raw_arguments = completion.choices[0].message.function_call.arguments
    return raw_arguments

#summarize_speech("what is the dual mandate")

def get_pc():
    pc = Pinecone(api_key="pcsk_36hKfz_6GL8ztjrsZZicZyCdeUZkEV1D3fBAcooULof9ZZ8zSq9wjjTA6BNKoE1en36KRU")
    return pc


@functools.lru_cache()
def similarity_search_with_relevance_scores_pinecone(query, top_k):
    """
    Query Pinecone index for similar vectors and return results with relevance scores.

    Args:
        query (str): The query text to find similar items for.
        top_k (int): Number of top results to return.

    Returns:
        list of tuples: Each tuple contains (result metadata, relevance score).
    """
    # Generate query embedding
    query_embedding = get_openai_embedding(query)
    pc = get_pc()
    index = pc.Index(name="maxent")
    results = index.query(vector=query_embedding, top_k=top_k, include_metadata=True)

    # Process results to return metadata and relevance scores
    processed_results = [
        (match["metadata"], match["score"])
        for match in results["matches"]
    ]
    return processed_results

# similarity_search_with_relevance_scores_pinecone("what is the dual mandate?", top_k=30)
