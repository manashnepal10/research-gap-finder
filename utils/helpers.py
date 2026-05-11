import os

def format_docs(docs):
    return "\n\n".join([doc.page_content for doc in docs])

def save_uploaded_file(uploaded_file):
    TEMP_DIR = "temp/"
    os.makedirs(TEMP_DIR, exist_ok=True)
    full_file_path = os.path.join(TEMP_DIR, uploaded_file.name)

    with open(full_file_path, "wb") as f:
        f.write(uploaded_file.read())
    
    return full_file_path