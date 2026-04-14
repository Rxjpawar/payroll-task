from src.ai.document_processor import load_and_split_pdf
from src.ai.vector_store import policy_qdrant_store
from src.ai.vector_store import payslip_qdrant_store


def index_payslip(file_path: str, metadata: dict):

    docs = load_and_split_pdf(file_path)

    # attaching metadata to each chunk
    for doc in docs:
        doc.metadata.update(metadata)

    vector_store = payslip_qdrant_store()

    vector_store.add_documents(docs)

    print("Payslip indexed successfully")


def index_policy(file_path: str, metadata: dict):

    docs = load_and_split_pdf(file_path)

    # attaching metadata to each chunk
    for doc in docs:
        doc.metadata.update(metadata)

    vector_store = policy_qdrant_store()

    vector_store.add_documents(docs)

    print("Policy indexed successfully")    