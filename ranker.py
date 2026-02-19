import math
from collections import defaultdict
from config import K1, B
from inverted_index import InvertedIndex
from tokenizer import tokenize

def rank_documents(query: str, index: InvertedIndex) -> list[tuple[int, float]]:
    
    scores = defaultdict(float)
    bm25_scores(query, index, scores)
    boost_scores(query, index, scores)

    scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return scores

def bm25_scores(query: str, index: InvertedIndex, scores: defaultdict) -> defaultdict:
    tokens = tokenize(query)
    avg_doc_length = compute_avg_doc_length(index)
    for token in tokens:
        if token not in index.postings:
            continue

        idf = compute_idf(token, index)
        postings = index.postings[token]

        update_bm25_score(index, postings, avg_doc_length, idf, scores)

    return scores

def update_bm25_score(index: InvertedIndex, postings: dict, avg_doc_length: float, idf: float, scores: defaultdict) -> float:
    for doc_id, info in postings.items():
        doc_len = index.document_lengths[doc_id]
        tf = info["frequency"]

        denominator = tf + K1 * (1 - B + B * (doc_len / avg_doc_length))
        score = idf * ((tf * (K1 + 1)) / denominator)

        scores[doc_id] += score

# Computation Helpers

# BM25
def compute_avg_doc_length(index: InvertedIndex) -> float:
    return index.total_terms / index.document_count if index.document_count else 0

def compute_idf(token: str, index: InvertedIndex) -> float:
    doc_freq = len(index.postings.get(token, {}))
    return math.log((index.document_count - doc_freq + 0.5) / (doc_freq + 0.5) + 1)

# Boosters

def boost_scores(query: str, index: InvertedIndex, scores: defaultdict) -> None:
    full_matches = full_phrase_match(query, index)
    # partial_matches = partial_phrase_match(query, index )
    # proximity_boosts = proximity_boost(query, index)

    for doc_id in full_matches:
        scores[doc_id] *= 1.5  # Full phrase match boost

    # for doc_id in partial_matches:
    #     scores[doc_id] *= 1.2  # Partial phrase match boost

    # for doc_id in proximity_boosts:
    #     scores[doc_id] *= (1 + proximity_boosts[doc_id])  # Proximity boost

def get_common_docs(query: str, index: InvertedIndex) -> set[int]:
    query_tokens = tokenize(query)
    common = set(index.postings.get(query_tokens[0], {}).keys())
    for token in query_tokens:
        common &= set(index.postings.get(token, {}).keys())
        if not common:
            break
    return common



def get_terms_positions(query: str, doc_id: str, index: InvertedIndex) -> set[int]:
    tokens = tokenize(query)

    terms_positions = []
    for token in tokens:
        postings = index.postings.get(token, {}) 
        positions = postings.get(doc_id, {}).get('positions', [])
        terms_positions.append(positions) if positions else None

    return terms_positions

def match_found(terms_positions: list[set[int]]) -> bool:
    primary_positions = terms_positions[0]
    for i in range(1, len(terms_positions)):
        token_positions = terms_positions[i]
        new_positions = matches(primary_positions, token_positions, i)
        if not new_positions:
            return False
        primary_positions = new_positions
    return True

def full_phrase_match(query: str, index: InvertedIndex) -> list[int]:
    common_docs = get_common_docs(query, index)

    results = []
    for doc_id in common_docs:
        terms_positions = get_terms_positions(query, doc_id, index)
        if match_found(terms_positions):
            results.append(doc_id)

    return results

def partial_phrase_match(query: str, index: InvertedIndex) -> list[int]:
    pass

def proximity_boost(query: str, index: InvertedIndex) -> list[int]:
    pass

def matches(primary_positions: set[int], token_positions: set[int], distance: int = 1) -> set[int]:
    new_positions = {p + distance for p in primary_positions}
    new_positions &= token_positions
    return new_positions