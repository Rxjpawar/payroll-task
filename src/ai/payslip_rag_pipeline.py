import os
from dotenv import load_dotenv
from openai import OpenAI
from src.ai.vector_store import payslip_qdrant_store

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
            f"Month: {doc.metadata.get('month', '')}\n"
            f"Year: {doc.metadata.get('year', '')}\n"
        )

    return "\n\n".join(context_parts)


def retrieve_docs(query: str, user_id: str):
    vector_store = payslip_qdrant_store()

    results = vector_store.similarity_search(
        query,
        k=5,
        filter={
            "must": [
                {
                    "key": "metadata.user_id",
                    "match": {"value": user_id}
                }
            ]
        }
    )

    return results


def generate_answer(query: str, context: str):
    SYSTEM_PROMPT = f"""
You are an AI payroll assistant.

    IMPORTANT RULES:
    - Answer ONLY from the given context
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


def run_rag_pipeline(query: str, user_id: str):
    docs = retrieve_docs(query, user_id)

    if not docs:
        return "No relevant payroll records found."

    context = build_context(docs)

    answer = generate_answer(query, context)

    return answer