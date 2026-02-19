from collections import defaultdict
import pickle
from tokenizer import tokenize


class InvertedIndex:
    def __init__(self):
        self.postings = defaultdict(dict)
        self.document_count = 0
        self.document_lengths = defaultdict(int)
        self.total_terms = 0
        
    
    def build_index(self, documents: dict[int, dict]):
        # in this tokenize doesnt return unique tokens but returns all tokens in the document, including duplicates. It may remove punctuation.
        # tokens is most likely a list of strings

        for doc_id in documents:
            tokens = tokenize(documents[doc_id]["content"])
            self.document_count += 1
            self.document_lengths[doc_id] = len(tokens)
            self.total_terms += len(tokens)

            for position, token in enumerate(tokens):
                if doc_id not in self.postings[token]:
                    self.postings[token][doc_id] = {'frequency': 0, 'positions': set()}
                
                entry = self.postings[token][doc_id]
                entry['frequency'] += 1
                entry['positions'].add(position)

    def save_index(self, file_path: str):
        with open(file_path, 'wb') as f:
            pickle.dump(self,f)
    
    @staticmethod
    def load_index(file_path: str):
        with open(file_path, 'rb') as f:
            return pickle.load(f)