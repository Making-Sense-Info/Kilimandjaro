from enum import StrEnum, auto
from dataclasses import dataclass
from typing import TypedDict
from urllib.parse import quote_plus
from chromadb.api.types import GetResult


class IDs(StrEnum):
    RUN = auto()
    SETDB = auto()
    PRE = auto()
    INFO = auto()
    PROGRESS = auto()
    EXIT = auto()


@dataclass
class State:
    db_setup: bool = False
    data_loaded: bool = False


@dataclass
class SPARQLQuery:
    """A SPARQL query with a label"""

    name: str
    value: str

    def encoded(self):
        return quote_plus(self.value)


class CCAMActe(TypedDict):
    code: str
    label: str


class SnomedTerm(TypedDict):
    code: str
    label: str


class LoincItem(TypedDict):
    code: str
    label: str


class CollectionInfo(TypedDict):
    """Represents the info we get from a Chroma DB collection"""

    name: str
    count: int
    peek: GetResult
