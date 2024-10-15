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
    # WIP since there are some bugs / limits with the number of documents
    # that can be indexed, we are batching here
    # see https://github.com/chroma-core/chroma/issues/1049
    batch_index = 0
    batch_index_end = batch_index + step
    while batch_index <= len(documents):
        end = min(batch_index_end, len(documents) + 1)
        subdocs = documents[batch_index:end]
        subids = ids[batch_index:end]
        if subdocs == []:
            break  # ??? xx = list(range(11)) ; xx[11:11] == []
        print(f"indexing documents from {batch_index} to {end-1}")
        add_to_collection(collection_name, subdocs, subids)
        batch_index = batch_index + step
        batch_index_end = batch_index + step


def query(collection_name: str, text: str) -> QueryResult:
    """Thin wrapper around `collection.query` in ChromaDB API.
    See https://docs.trychroma.com/reference/py-collection#query"""
    collection = client.get_collection(collection_name)
    results = collection.query(query_texts=text)
    return results


def delete_collection(name: str):
    """Thin wrapper around ChromaDB API"""
    client.delete_collection(name)
