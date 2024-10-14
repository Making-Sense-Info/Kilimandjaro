# Kilimandjaro

Kilimandjaro is a program that provides mapping from any labels to medical terminologies.

<SCREENSHOT FROM THE WEB UI>

Currently two sources are used:
  - the french Snomed CT
  - the CCAM terminology

In order to provide a useful mapping, we compare text [embeddings](https://huggingface.co/blog/getting-started-with-embeddings).

The main way to use Kilimandjaro is to:
1. produce and store embeddings
2. query through the UI.

Before anything:
  - install [rye]() (several methods here, there's a [homebrew formula](https://formulae.brew.sh/formula/rye#default))
  - run `rye sync` at the root of this repo directory
  - copy the `config-skeleton.toml` file to have a dedicated `config.toml` in which you provide actual values
    - `rye run indexer config` will display the configuration sections (more on how to complete below)

To produce the embeddings - here for the CCAM data source:

```shell
rye run indexer add ccam
```

It will fetch the source data, produce and store the embeddings in a local [ChromaDB](https://www.trychroma.com) instance.

For this source, the whole process is several minutes long.

Then launch the web UI:

```shell
rye run webui
```

## Architecture

The three main pieces of this application are:
  - the vector database, using ChromaDB, to produce and store embeddings
  - the indexer program, which fetch source data and push them to ChromaDB
  - the web UI, which allows humans to really use the application

The indexer is a command line

## Notes

### CCAM

- when parsing the JSON payload outside with `rye run indexer add ccam | yq` some errors appears
 - for example for this acte: `{'code':'MBFA001', 'label': 'Résection "en bloc" d\'une extrémité et/ou de la diaphyse de l\'humérus'}`
 - this would be a better encoding: `"label":"Résection \"en bloc\" d\\'une extrémité et/ou de la diaphyse de l\\'humérus"`?
