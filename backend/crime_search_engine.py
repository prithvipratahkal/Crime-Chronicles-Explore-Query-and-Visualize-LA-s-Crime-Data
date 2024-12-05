import json
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import os
import torch

class CrimeSearchEngine:
    def __init__(self, embeddings_file: str, metadata_file: str, model_name: str = "all-MiniLM-L6-v2", hf_token: str = None):
        """
        Initialize the search engine with file paths and model configuration.
        """
        self.embeddings_file = embeddings_file
        self.metadata_file = metadata_file
        self.model_name = model_name
        self.hf_token = hf_token
        self.embeddings = None
        self.metadata = None
        self.faiss_index = None
        self.model = None

    def load_embeddings_and_metadata(self):
        """
        Load embeddings from .npy file and metadata from a line-delimited JSON file.
        """
        # Load embeddings
        self.embeddings = np.load(self.embeddings_file)
        print(f"Loaded embeddings from {self.embeddings_file}")

        # Load metadata
        self.metadata = []
        with open(self.metadata_file, "r") as metafile:
            for line in metafile:
                self.metadata.append(json.loads(line.strip()))
        print(f"Loaded metadata from {self.metadata_file} with {len(self.metadata)} entries")

    def initialize_model(self):
        """
        Initialize the SentenceTransformer model for query embeddings.
        """
        self.model = SentenceTransformer(self.model_name, use_auth_token=self.hf_token)
    
        # Use GPU if available, otherwise fall back to CPU
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = self.model.to(device)
        print(f"Model loaded and moved to {device}.")

    def create_faiss_index(self):
        """
        Create a FAISS index from the loaded embeddings.
        """
        if self.embeddings is None:
            raise ValueError("Embeddings not loaded. Call load_embeddings_and_metadata first.")
        embedding_dim = self.embeddings.shape[1]
        self.faiss_index = faiss.IndexFlatL2(embedding_dim)
        self.faiss_index.add(self.embeddings)
        print(f"FAISS index created with {self.faiss_index.ntotal} embeddings.")

    def query_embeddings(self, query: str, k: int = 10):
        """
        Query the FAISS index for the top-k most similar embeddings.
        """
        if not self.faiss_index or not self.model:
            raise ValueError("FAISS index or model not initialized. Call setup first.")

        # Generate embedding for the query
        query_embedding = self.model.encode([query], convert_to_tensor=True, device="cuda").cpu().numpy()

        # Search for the top-k matches
        distances, indices = self.faiss_index.search(query_embedding, k)

        # Retrieve results
        results = [{"metadata": self.metadata[idx], "distance": distances[0][i]} for i, idx in enumerate(indices[0])]
        return results

    def setup(self):
        """
        Load embeddings, metadata, initialize the model, and create the FAISS index.
        """
        self.load_embeddings_and_metadata()
        self.initialize_model()
        self.create_faiss_index()
