from langchain_qdrant import QdrantVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": False}
)

COLLECTION_NAME = "payslip_vectors"
COLLECTION_NAME2 = "policy_vectors"

def payslip_qdrant_store():
    client = QdrantClient(url="http://localhost:6333")

    #creating the collection if it doesnt exist
    if COLLECTION_NAME not in [c.name for c in client.get_collections().collections]:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )

    return QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=embedding_model,
    )

def policy_qdrant_store():
    client = QdrantClient(url="http://localhost:6333")

    #creating the collection if it doesnt exist
    if COLLECTION_NAME2 not in [c.name for c in client.get_collections().collections]:
        client.create_collection(
            collection_name=COLLECTION_NAME2,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )

    return QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME2,
        embedding=embedding_model,
    )