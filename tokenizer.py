import re
from config import STOP_WORDS

def tokenize(text):
    # As of now it just finds words without punctuation and lowercases them

    text = text.lower()
    tokens = re.findall(r"\b[a-z]+\b", text)
    # tokens = list(filter(lambda t: t not in STOP_WORDS, tokens))
    return tokens
