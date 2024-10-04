# kilimandjaro

Constances terms to Snomed.

Synopsis:

- get category scheme from a DDI L questionnaire
- get Snomed terminology from a graph store
- produce embeddings
- per item in the scheme, search the n most relevant Snomed terms

Simplest approach:

- use chromadb for indexing https://docs.trychroma.com/getting-started
- and llama 3.1 embeddings using ollama https://docs.trychroma.com/integrations/ollama
