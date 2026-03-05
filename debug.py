import chromadb

client = chromadb.PersistentClient(path="./chroma_db")  # il tuo path

# Lista tutte le collection
print(client.list_collections())

# Seleziona la collection
collection = client.get_collection("nome_collection")

# Numero totale di chunk
print(collection.count())


results = collection.get(
    where={"source": "nome_libro.pdf"},  # dipende dai tuoi metadata
    include=["metadatas"]
)
print(len(results["ids"]))