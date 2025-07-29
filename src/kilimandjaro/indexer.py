"""
This module holds the top level function for managing the index, ie the data inside the ChromaDB instance.
"""

from configparser import ConfigParser
from kilimandjaro.db import (
    add_to_collection,
    batch_update,
    list_collections,
    delete_collection,
)
from kilimandjaro.source import (
    get_ccam_actes,
    ccam_acte_query,
    get_snomed_terms,
    snomed_random_query,
    get_loinc_items
)
import fire
from rich import print as rprint
from rich.tree import Tree


# --- Print helpers
def ongoing(text):
    rprint(f"[bold yellow]>[/] {text}.")


def ok(text):
    rprint(f"[bold green]√[/] {text}.")


def err(text):
    rprint(f"[bold red]X[/] {text}.")


# --- Action functions


def del_collection(name: str):
    """Call the `db` module to delete a collection"""
    delete_collection(name)


def add_snomed():
    """WIP Currently only a small fraction of Snomed CT"""
    ongoing("Fetching Snomed data")
    res = get_snomed_terms(snomed_random_query)
    documents = [term["label"] for term in res]
    ids = [term["code"] for term in res]
    ongoing("Adding to collection")
    batch_update("snomed", documents, ids)


def add_ccam_actes():
    """Create a CCAM actes collection"""
    ongoing("Fetching ccam data")
    actes_data = get_ccam_actes(ccam_acte_query)
    documents = [acte["label"] for acte in actes_data]
    ids = [acte["code"] for acte in actes_data]
    ongoing("Adding to collection")
    batch_update("ccam", documents, ids)

def add_loinc():
    ongoing("Fetching Loinc")
    items = get_loinc_items()
    documents = [item["label"] for item in items]
    ids = [item["code"] for item in items]
    ongoing("Adding to collection")
    batch_update("loinc", documents, ids)

# --- CLI


def add(source):
    """Add data to ChromaDB"""
    match source:
        case "ccam":
            add_ccam_actes()
        case "snomed":
            add_snomed()
        case "loinc":
            add_loinc()
        case _:
            err(f"{source} is not a valid option")


def clean(collection_name: str):
    """Clean the DB. Currently only support the deletion of a collection."""
    if collection_name in list_collections():
        ongoing(f"Cleaning collection {collection_name}")
        delete_collection(collection_name)
        ok("Done.")
    else:
        err(f"{collection_name} collection doesn't exist")


def config():
    """Provides configuration information"""
    conf = ConfigParser()
    conf.read("config.toml")
    conf_sections = Tree("[bold blue]¬[/] Configuration sections")
    for section in conf.sections():
        conf_sections.add(str(section))
    print(conf_sections)


def check():
    """For now, this command is use to perform dev check."""
    ok("No checks for now")


if __name__ == "__main__":
    fire.Fire(
        {
            "add": add,
            "check": check,
            "clean": clean,
            "config": config,
        }
    )
