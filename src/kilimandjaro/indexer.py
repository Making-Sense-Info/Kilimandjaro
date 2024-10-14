"""
This module holds the top level function for managing the index, ie the data inside the ChromaDB instance.
"""

from configparser import ConfigParser
from kilimandjaro.db import add_to_collection
from kilimandjaro.source import get_ccam_actes, ccam_acte_query
import fire


def clean_index():
    pass


def add_ccam_actes():
    """Create a CCAM actes collection"""
    print("fetching ccam data")
    actes_data = get_ccam_actes(ccam_acte_query)
    documents = [acte["label"] for acte in actes_data]
    ids = [acte["code"] for acte in actes_data]
    print("adding to collection")
    # WIP since there are some bugs / limits with the number of documents
    # that can be indexed, we are batching here
    # see https://github.com/chroma-core/chroma/issues/1049
    batch_index = 0
    batch_index_end = batch_index + 500
    while batch_index <= len(documents):
        end = min(batch_index_end, len(documents) + 1)
        subdocs = documents[batch_index:end]
        subids = ids[batch_index:end]
        print(f"indexing documents from {batch_index} to {end-1}")
        add_to_collection("ccam", subdocs, subids)
        batch_index = batch_index + 500
        batch_index_end = batch_index + 500


def add(source):
    """Add data to ChromaDB"""
    match source:
        case "ccam":
            add_ccam_actes()
        case "snomed":
            print("Work in progress.")
        case _:
            print(f"{source} is not a valid add option.")


def config():
    """Provides configuration information"""
    conf = ConfigParser()
    conf.read("config.toml")
    print("Configuration sections:")
    for section in conf.sections():
        print(f"- {section}")


def check():
    """For now, this command is use to perform dev check."""
    get_ccam_actes(ccam_acte_query)


if __name__ == "__main__":
    fire.Fire({"add": add, "config": config, "check": check})
