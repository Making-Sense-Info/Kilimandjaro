import xml.etree.ElementTree as et
from pathlib import Path
from xml.etree.ElementPath import findall
import httpx
from urllib.parse import quote_plus
from dataclasses import dataclass
from kilimandjaro.models import SPARQLQuery

namespaces = {"l": "ddi:logicalproduct:3_3", "r": "ddi:reusable:3_3"}


snomed_tension_query = SPARQLQuery(
    "Contient `tension`",
    """
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX sct-ext: <http://data.esante.gouv.fr/NRC-France/sct-ext#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
select ?disorder ?label where {
	?disorder dc:type "disorder" .
    ?disorder rdfs:label ?label
    FILTER langMatches(lang(?label), "fr")
    FILTER contains(?label, "tension")
}
""",
)

snomed_random_query = SPARQLQuery(
    "Aléa, les 500 premiers",
    """
PREFIX dc: <http://purl.org/dc/elements/1.1/>
select ?disorder ?random ?label where {
	?disorder dc:type "disorder" .
	?disorder rdfs:label ?label
	FILTER langMatches(lang(?label), "fr")
    BIND(RAND() as ?random)
} order by ?random limit 1000
""",
)


async def get_category_scheme_from_ddi(source_file_path: Path) -> list[str]:
    with open(source_file_path) as sf:
        tree = et.parse(sf)
        root = tree.getroot()
        category_schemes = root.findall(
            ".//l:CategoryScheme[r:ID='CategoryScheme-lzmgjrzf']", namespaces=namespaces
        )
        # [r:Label/r:Content='L_AFFECT_CV'] doesn't work because of the [tag] support limitation ->
        # https://docs.python.org/3/library/xml.etree.elementtree.html#supported-xpath-syntax
        cs = category_schemes.pop()
        categories = []
        for cat in cs.findall("l:Category", namespaces=namespaces):
            label = cat.findall("r:Label/r:Content", namespaces=namespaces).pop().text
            categories.append(label)
        return categories


async def get_snomed_terms(query: SPARQLQuery):
    """From GraphDB but with filter in order to limit what we work with.
    We should also have an alternative that download everything on disk once?"""
    target = f"https://graphdb.linked-open-statistics.org/repositories/snomed?query={quote_plus(query.value)}"

    resp = httpx.get(target, headers={"Accept": "application/sparql-results+json"})
    res = resp.json()
    final_res = [terms["label"]["value"] for terms in res["results"]["bindings"]]
    return final_res
