import chromadb


# Create a persistent ChromaDB client
client = chromadb.PersistentClient(
    path="./chroma_db"
)


# Create or load our knowledge collection
collection = client.get_or_create_collection(
    name="project_knowledge"
)


def add_knowledge(document_id, text):
    collection.add(
        ids=[document_id],
        documents=[text]
    )


if __name__ == "__main__":

    with open(
        "knowledge/coding_standards.txt",
        "r",
        encoding="utf-8"
    ) as file:

        document = file.read()


    add_knowledge(
        "coding_standards",
        document
    )


    print("Knowledge added successfully!")