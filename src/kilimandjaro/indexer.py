"""
This module holds the top level function for managing the index, ie the data inside the ChromaDB instance.
"""
from kilimandjaro.source import get_ccam_actes, ccam_acte_query
import fire

def clean_index():
    pass

def add_ccam_actes():
    """Create a CCAM actes collection"""
    actes_data = get_ccam_actes(ccam_acte_query)
    print(actes_data)

def add(thing):
    match thing:
        case "ccam":
            add_ccam_actes()
        case _:
            print(f"{thing} is not a valid add option.")

if __name__ == "__main__":
    fire.Fire({
        "add" : add
    })
