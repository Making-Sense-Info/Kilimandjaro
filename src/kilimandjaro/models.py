from enum import StrEnum, auto
from dataclasses import dataclass

class IDs(StrEnum):
    RUN = auto()
    SETDB = auto()
    PRE = auto()
    INFO = auto()
    PROGRESS = auto()
    EXIT = auto()

@dataclass
class State():
    db_setup: bool = False
    data_loaded: bool = False


@dataclass
class SPARQLQuery():
    """ A SPARQL query with a label """
    name: str
    value: str
