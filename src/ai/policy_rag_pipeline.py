import os
from dotenv import load_dotenv
from openai import OpenAI
from src.ai.vector_store import policy_qdrant_store

from src.utils.cache import generate_cache_key,get_cached_response,set_cached_response

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def build_context(docs):
    context_parts = []

    for doc in docs:
        context_parts.append(
            f"Content: {doc.page_content}\n"
            f"Year: {doc.metadata.get('year', '')}\n"
            f"Name: {doc.metadata.get('name', '')}\n"
            f"Page number: {doc.metadata.get('page_label', '')}\n"
        )

    return "\n\n".join(context_parts)


def retrieve_docs(query: str,):
    vector_store = policy_qdrant_store()

    results = vector_store.similarity_search(
        query,
        k=5,
        filter={
            "must": [
                {
                    "key": "metadata.type",
                    "match": {"value":"policy"}
                }
            ]
        }
    )

    return results


def generate_answer(query: str, context: str):
    SYSTEM_PROMPT = f"""
    You are an AI policy assistant.

    IMPORTANT RULES:
    - Answer ONLY from the given context
    - Explain asked policies to user
    - Do NOT hallucinate
    - If data is missing, say: "No record found"
    - Keep answer simple and human-readable
    - Sound like you are a human 

Context:
{context}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ]
    )

    return response.choices[0].message.content


def run_policy_rag_pipeline(query: str):
    cache_key = f"policy:{query.strip().lower()}"

    cached = get_cached_response(cache_key)
    if cached:
        print("policy Cache Hit horaaaaa")
        return cached["response"]

    print("policy cache miss hogaaya lol")

    docs = retrieve_docs(query)

    if not docs:
        return "No relevant payroll records found."

    context = build_context(docs)

    answer = generate_answer(query, context)
    print("saving the cache")
    set_cached_response(cache_key, {"response": answer})
    return answer