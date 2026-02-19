# Search Engine with BM25 and Phrase Matching

Built a from-scratch search engine indexing ~19,000 documents using a positional inverted index and BM25 ranking. Designed to explore core information retrieval systems without external search frameworks.

---

## How to Run

1. Place documents inside the target data folder.
2. Run: main.py

- On first run, the index will be built and serialized (~2 minutes).
- On subsequent runs, the serialized index is loaded instantly.

---

## Features

### Positional Inverted Index

- Stores term frequency and positions per document
- Enables efficient exact phrase matching

### BM25 Ranking

- Implemented full BM25 scoring
- Includes term frequency saturation and document length normalization
- Replaced earlier TF-IDF implementation after evaluation

### Phrase Boosting

- Exact phrase matches are boosted using positional intersection

### Index Serialization

- Cold indexing (~2 minutes) avoided on subsequent runs
- Index saved and loaded using `pickle`
- Mimics offline indexing used in production search systems

---

## Architecture

Modular structure for clarity and extensibility:

- main.py
- document_loader.py
- tokenizer.py
- inverted_index.py
- ranker.py
- config.py

Separation of concerns allows:

- Independent ranking experimentation (TF-IDF → BM25)
- Isolated performance tuning
- Easier feature additions

---

## Performance

- Corpus size: ~19,000 documents
- Cold index build time: ~2 minutes (I/O bound)
- Query execution: in-memory lookup + BM25 scoring

---

## Skills Demonstrated

- Information Retrieval fundamentals
- Algorithm implementation (BM25)
- Positional indexing
- Data structure tradeoff analysis (dict vs object postings)
- Modular Python system design
