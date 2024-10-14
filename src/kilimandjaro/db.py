from typing_extensions import TypedDict
import chromadb
from chromadb.api.types import GetResult

client = chromadb.PersistentClient()


class CollectionInfo(TypedDict):
    """Represents the info we get from a Chroma DB collection"""

    count: int
    peek: GetResult


def list_collections() -> dict[str, GetResult]:
    collections = {}
    for collection in client.list_collections():
        peek = collection.peek()  # TODO should be optional
        count = collection.count()
        collections[collection.name] = CollectionInfo(count=count, peek=peek)

    return collections


def add_to_collection(collection_name, documents, ids):
    collection = client.get_or_create_collection(collection_name)
    collection.add(documents=documents, ids=ids)
