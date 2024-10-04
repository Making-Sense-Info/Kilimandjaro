# Kilimandjaro

This is a proof-of-concept: mapping Constances terms to Snomed CT.

The basis for this mapping is producing [embeddings](https://huggingface.co/blog/getting-started-with-embeddings) for both the Constances terms and the Snomed CT terms and use a distance function to fetch the most relevant ones.

More precisely, this program:

- get a category scheme from questionnaire represented using DDI Lifecycle
- fetch the Snomed terminologies from a graph store
- produce [embeddings using ChromaDB](https://docs.trychroma.com)
- per item in the scheme, display the `n` most relevant Snomed terms

Currently, the program is displayed as a [TUI](https://en.wikipedia.org/wiki/Text-based_user_interface) application using [textualize](https://textual.textualize.io).
