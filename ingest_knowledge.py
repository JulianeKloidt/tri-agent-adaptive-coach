import chromadb
from chromadb.utils import embedding_functions
import os

# 1. Setup the Database
db_path = "./db"
chroma_client = chromadb.PersistentClient(path=db_path)

# 2. Use a local embedding function
default_ef = embedding_functions.DefaultEmbeddingFunction()

collection = chroma_client.get_or_create_collection(
    name="triathlon_rules", 
    embedding_function=default_ef
)

# 3. Read the data with error checking
file_path = "data/coaching_rules.txt"

if not os.path.exists(file_path):
    print(f"❌ Error: I can't find the file at {file_path}. Make sure the 'data' folder exists!")
else:
    with open(file_path, "r") as f:
        lines = f.readlines()
        rules = [line.strip() for line in lines if len(line.strip()) > 5]

    if not rules:
        print("❌ Error: The text file is empty. Add some rules first!")
    else:
        # 4. Store them
        print(f"Attempting to add {len(rules)} rules to the database...")
        collection.add(
            documents=rules,
            ids=[f"rule_{i}_{int(os.path.getmtime(file_path))}" for i in range(len(rules))]
        )
        print(f"✅ Indexed {len(rules)} coaching rules into the local database.")