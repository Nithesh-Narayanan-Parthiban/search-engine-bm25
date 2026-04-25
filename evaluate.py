from datasets import load_dataset
from beir.retrieval.evaluation import EvaluateRetrieval

from inverted_index import InvertedIndex
from ranker import rank_documents


def load_from_huggingface():
    print("Loading corpus...")
    corpus_ds = load_dataset("BeIR/nfcorpus", "corpus", split="corpus")
    print("Loading queries...")
    queries_ds = load_dataset("BeIR/nfcorpus", "queries", split="queries")
    print("Loading qrels...")
    qrels_ds = load_dataset("BeIR/nfcorpus-qrels", split="test")

    corpus = {row["_id"]: {"title": row["title"], "text": row["text"]} for row in corpus_ds}
    queries = {row["_id"]: row["text"] for row in queries_ds}
    qrels = {}
    for row in qrels_ds:
        qrels.setdefault(row["query-id"], {})[row["corpus-id"]] = int(row["score"])

    return corpus, queries, qrels


def load_beir_corpus(corpus: dict) -> dict:
    """Converts BEIR corpus format to your document format."""
    documents = {}
    for doc_id, doc in corpus.items():
        documents[doc_id] = {
            "title": doc.get("title", ""),
            "content": doc.get("title", "") + " " + doc.get("text", "")
        }
    return documents


def build_or_load_index(documents: dict, index_path: str = "beir_index.pkl") -> InvertedIndex:
    import os
    if os.path.exists(index_path) and os.path.getsize(index_path) > 0:
        print("Loading existing BEIR index...")
        return InvertedIndex.load_index(index_path)

    print("Building index on BEIR corpus...")
    index = InvertedIndex()
    index.build_index(documents)
    index.save_index(index_path)
    print("Index built and saved.")
    return index


def run_evaluation():
    # 1. Load dataset from HuggingFace
    corpus, queries, qrels = load_from_huggingface()
    print(f"Loaded {len(corpus)} docs, {len(queries)} queries.")

    # 2. Convert corpus to your format and build index
    documents = load_beir_corpus(corpus)
    index = build_or_load_index(documents)

    # 3. Run all queries through your ranker
    print("Running queries...")
    run = {}
    for query_id, query_text in queries.items():
        results = rank_documents(query_text, index)
        run[query_id] = {doc_id: score for doc_id, score in results}

    # 4. Evaluate
    evaluator = EvaluateRetrieval()
    ndcg, _map, recall, precision = evaluator.evaluate(qrels, run, k_values=[10])

    print("\n========== RESULTS ==========")
    print(f"nDCG@10:      {ndcg['NDCG@10']:.4f}")
    print(f"MAP@10:       {_map['MAP@10']:.4f}")
    print(f"Recall@10:    {recall['Recall@10']:.4f}")
    print(f"Precision@10: {precision['P@10']:.4f}")
    print("==============================")
    print("\nExpected BM25 baseline on NFCorpus: nDCG@10 ≈ 0.30–0.34")
    return ndcg['NDCG@10']


if __name__ == "__main__":
    run_evaluation()