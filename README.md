# Kilimandjaro

This is a proof-of-concept: mapping Constances terms to Snomed CT.

The basis for this mapping is producing [embeddings](https://huggingface.co/blog/getting-started-with-embeddings) for both the Constances terms and the Snomed CT terms and use a distance function to fetch the most relevant ones.

More precisely, this program:

- get a category scheme from questionnaire represented using DDI Lifecycle
- fetch the Snomed terminologies from a graph store
- produce [embeddings using ChromaDB](https://docs.trychroma.com)
- per item in the scheme, display the `n` most relevant Snomed terms

Currently, the program is displayed as a [TUI](https://en.wikipedia.org/wiki/Text-based_user_interface) application using [textualize](https://textual.textualize.io).

## Next

To generalise:

- the app will be a simple webapp (using Streamlit)
- enter a text (see above), compare to a Snomed CT or another vocab (CCAM ?)

Two possibles program:

- the webapp
- the indexer


## Notes

### CCAM

- when parsing the JSON payload outside with `rye run indexer add ccam | yq` some errors appears
 - for example for this acte: `{'code': 'MBFA001', 'label': 'Résection "en bloc" d\'une extrémité et/ou de la diaphyse de l\'humérus'}`
