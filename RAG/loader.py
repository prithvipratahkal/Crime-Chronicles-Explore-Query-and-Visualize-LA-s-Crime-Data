import json
import numpy as np
from sentence_transformers import SentenceTransformer
import os
import faiss

# Hugging Face Token
HF_TOKEN = "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"
os.environ["HF_TOKEN"] = HF_TOKEN

# Generate embeddings for sentences
def generate_embeddings(sentences, model_name='all-MiniLM-L6-v2', use_auth_token=None):
    model = SentenceTransformer(model_name, use_auth_token=use_auth_token)
    model = model.to("cuda")  # Use GPU if available
    embeddings = model.encode(sentences, convert_to_tensor=True, device="cuda").cpu().numpy()
    return embeddings

# Save metadata as line-delimited JSON
def save_metadata_line_delimited(metadata, metadata_file):
    """
    Save metadata as line-delimited JSON, where each line is a separate JSON object.
    """
    with open(metadata_file, "w") as metafile:
        for obj in metadata:
            metafile.write(json.dumps(obj) + "\n")  # Write each JSON object on a new line
    print(f"Metadata saved to {metadata_file} in line-delimited format")

# Load JSON and generate embeddings
def create_embeddings_store(input_file, embeddings_file, metadata_file, model_name='all-MiniLM-L6-v2'):
    """
    Reads a JSON file line-by-line, generates embeddings, and saves them along with the metadata.
    """
    sentences = []
    metadata = []

    # Read the JSON file line-by-line
    with open(input_file, "r") as infile:
        for line in infile:
            obj = json.loads(line.strip())  # Parse each line as JSON
            sentences.append(obj["sentence"])  # Extract the sentence for embedding
            metadata.append(obj)  # Store the entire JSON object as metadata

    # Generate embeddings
    embeddings = generate_embeddings(sentences, model_name=model_name, use_auth_token=HF_TOKEN)

    # Save embeddings to disk
    np.save(embeddings_file, embeddings)
    print(f"Embeddings saved to {embeddings_file}")

    # Save metadata to disk in line-delimited JSON format
    save_metadata_line_delimited(metadata, metadata_file)

# Paths for files
input_file = "data.json"         # Input JSON file
embeddings_file = "embeddings.npy"  # File to store embeddings
metadata_file = "metadata.json"     # File to store metadata

# Create and store embeddings
create_embeddings_store(input_file, embeddings_file, metadata_file)

# Load embeddings and metadata
def load_embeddings_and_metadata(embeddings_file, metadata_file):
    """
    Load embeddings from .npy file and metadata from a line-delimited JSON file.

    Args:
        embeddings_file (str): Path to the .npy file containing embeddings.
        metadata_file (str): Path to the line-delimited JSON file.

    Returns:
        tuple: A tuple of (embeddings, metadata), where metadata is a list of JSON objects.
    """
    # Load embeddings
    embeddings = np.load(embeddings_file)
    print(f"Loaded embeddings from {embeddings_file}")

    # Load metadata line-by-line
    metadata = []
    with open(metadata_file, "r") as metafile:
        for line in metafile:
            metadata.append(json.loads(line.strip()))  # Parse each line as JSON object
    print(f"Loaded metadata from {metadata_file} with {len(metadata)} entries")

    return embeddings, metadata

# Create FAISS index from embeddings
def create_faiss_index(embeddings):
    embedding_dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(embedding_dim)  # L2 (Euclidean) distance
    index.add(embeddings)  # Add embeddings to the index
    print(f"FAISS index created with {index.ntotal} embeddings")
    return index

# Query the FAISS index
def query_embeddings(index, query, metadata, model_name='all-MiniLM-L6-v2', k=10):
    # Load model and generate query embedding
    model = SentenceTransformer(model_name, use_auth_token=HF_TOKEN)
    model = model.to("cuda")  # Use GPU if available
    query_embedding = model.encode([query], convert_to_tensor=True, device="cuda").cpu().numpy()

    # Search for the top-k matches
    distances, indices = index.search(query_embedding, k)

    # Retrieve and return results
    results = [{"metadata": metadata[idx], "distance": distances[0][i]} for i, idx in enumerate(indices[0])]
    return results

# Paths for files
embeddings_file = "embeddings.npy"
metadata_file = "metadata.json"

# Load embeddings and metadata
embeddings, metadata = load_embeddings_and_metadata(embeddings_file, metadata_file)

# Create FAISS index
faiss_index = create_faiss_index(embeddings)

# Start Q&A session
print("\nStarting Q&A session. Type 'exit' to quit.")
while True:
    user_query = input("\nEnter your query: ")
    if user_query.lower() == "exit":
        break

    # Query embeddings
    results = query_embeddings(faiss_index, user_query, metadata, model_name='all-MiniLM-L6-v2', k=10)

    # Display results
    print("\nTop matches:")
    for result in results:
        print(f"Document: {result['metadata']['sentence']}")
        print(f"Distance: {result['distance']}\n")
