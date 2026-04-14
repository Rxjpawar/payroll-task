from src.ai.vector_store import get_qdrant_store


def get_retriever(user_id: str):
    vector_store = get_qdrant_store()

    retriever = vector_store.as_retriever(
        search_kwargs={
            "k": 4,
            "filter": {
                "must": [
                    {
                        "key": "metadata.user_id",
                        "match": {"value": user_id}
                    }
                ]
            }
        }
    )

    return retriever


def retrieve_context(query: str, user_id: str):
    retriever = get_retriever(user_id)

    docs = retriever.invoke(query)

    context = "\n\n".join([doc.page_content for doc in docs])

    return context