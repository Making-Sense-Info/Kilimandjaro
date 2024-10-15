import chromadb
from chromadb.api.types import ID, Document, QueryResult

from kilimandjaro.models import CollectionInfo

client = chromadb.PersistentClient()


def list_collections() -> dict[str, CollectionInfo]:
    """List available collection, storing info like the number of elements contained.
    For each collection, informations are stored in a `CollectionInfo` dict.
    Returns a dict which shape is `{"collection name": CollectionInfo}`"""
    collections = {}
    for collection in client.list_collections():
        peek = collection.peek()  # TODO should be optional
        count = collection.count()
        collections[collection.name] = CollectionInfo(
            name=collection.name, count=count, peek=peek
        )

    return collections


def add_to_collection(collection_name: str, documents: list[Document], ids: list[ID]):
    """Add documents and ids to a collection."""
    # TODO support metadatas ?
    collection = client.get_or_create_collection(collection_name)
    collection.add(documents=documents, ids=ids)


def batch_update(
    collection_name: str, documents: list[Document], ids: list[ID], step: int = 500
):
    """Add documents and ids to a collection by blocks of `step` size."""
    # TODO WIP
    pass


def query(collection_name: str, text: str) -> QueryResult:
    """Thin wrapper around `collection.query` in ChromaDB API.
    See https://docs.trychroma.com/reference/py-collection#query"""
    collection = client.get_collection(collection_name)
    results = collection.query(query_texts=text)
    return results
