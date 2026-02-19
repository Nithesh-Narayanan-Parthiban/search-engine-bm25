import os

def load_documents(folder_path, max_docs=None):
    documents = {}
    count = 0

    for entry in os.scandir(folder_path):
        if entry.is_file() and entry.name.endswith(".txt"):
            file_path = entry.path
            content = read_document(file_path)

            documents[entry.name] = {"title": entry.name, "content": content}

            count += 1
            if max_docs and count >= max_docs:
                break

    return documents

def read_document(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()