import os

from document_loader import load_documents
from inverted_index import InvertedIndex
from config import DOCUMENTS_PATH, INDEX_FILE_PATH, TOP_K_RESULTS, DOCUMENTS_SEARCH_COUNT
from ranker import rank_documents

def main():
    index,documents = preprocess_data()
    print("Ready. Type your query (type 'exit' to quit).")

    handle_query(index,documents)

def preprocess_data():
    print("Loading documents...")
    documents = load_documents(DOCUMENTS_PATH,DOCUMENTS_SEARCH_COUNT)

    print("Building index...")
    if os.path.exists(INDEX_FILE_PATH) and os.path.getsize(INDEX_FILE_PATH) > 0:
        print("Loading existing index...")
        index = InvertedIndex.load_index(INDEX_FILE_PATH)
    else:
        print("No existing index found. Building new index...")
        index = InvertedIndex()
        index.build_index(documents)
        index.save_index(INDEX_FILE_PATH)

    return index, documents

def handle_query(index: InvertedIndex, documents: dict[int, dict]):
    while True:
        query = input(">> ")

        if query.lower() in ["exit","quit","q"]:
            break

        results = rank_documents(query, index)

        print("\nTop Results:")
        for document, score in results[:TOP_K_RESULTS]:
            print(f"{documents[document]['title']} | Score: {score:.4f}")
        print() 

if __name__ == "__main__":
    main()