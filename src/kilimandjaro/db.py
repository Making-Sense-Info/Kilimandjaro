from typing_extensions import TypedDict
import chromadb
from chromadb.api.types import GetResult, QueryResult

client = chromadb.PersistentClient()


class CollectionInfo(TypedDict):
    """Represents the info we get from a Chroma DB collection"""
    name: str
    count: int
    peek: GetResult


def list_collections() -> dict[str, CollectionInfo]:
    collections = {}
    for collection in client.list_collections():
        peek = collection.peek()  # TODO should be optional
        count = collection.count()
        collections[collection.name] = CollectionInfo(name=collection.name, count=count, peek=peek)

    return collections


def add_to_collection(collection_name, documents, ids):
    collection = client.get_or_create_collection(collection_name)
    collection.add(documents=documents, ids=ids)

def query(collection_name, text) -> QueryResult:
    collection = client.get_collection(collection_name)
    results = collection.query(query_texts=text)
    return results
