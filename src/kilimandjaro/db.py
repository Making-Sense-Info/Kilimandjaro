import chromadb
from chromadb.api.types import QueryResult

from kilimandjaro.models import CollectionInfo

client = chromadb.PersistentClient()


def list_collections() -> dict[str, CollectionInfo]:
    collections = {}
    for collection in client.list_collections():
        peek = collection.peek()  # TODO should be optional
        count = collection.count()
        collections[collection.name] = CollectionInfo(
            name=collection.name, count=count, peek=peek
        )

    return collections


def add_to_collection(collection_name, documents, ids):
    collection = client.get_or_create_collection(collection_name)
    collection.add(documents=documents, ids=ids)


def query(collection_name, text) -> QueryResult:
    collection = client.get_collection(collection_name)
    results = collection.query(query_texts=text)
    return results
