from typing import List
from sentence_transformers import SentenceTransformer

class Embedder:
    """
    Local embedding generator using Sentence-Transformers.
    Fully offline, free, and compatible with pgvector.
    """

    def __init__(
        self,
        model_name: str = "BAAI/bge-large-en-v1.5",
        normalize: bool = True,
        device: str | None = None
    ):
        self.model = SentenceTransformer(model_name, device=device)
        self.normalize = normalize

    def embed_text(self, text: str) -> List[float]:
        """
        Embed a single text string.
        """
        embedding = self.model.encode(
            text,
            normalize_embeddings=self.normalize
        )
        return embedding.tolist()

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        embeddings = self.model.encode(
            texts,
            batch_size=16,
            normalize_embeddings=self.normalize,
            show_progress_bar=True,
            convert_to_numpy=True,
        )
        return embeddings.tolist()
    
    def embed_documents(self, docs: List[str]) -> List[List[float]]:
        """
        Embed multiple documents (batch embedding).
        This is MUCH faster than calling embed_text in a loop.
        """
        embeddings = self.model.encode(
            docs,
            normalize_embeddings=self.normalize,
            batch_size=16,
            show_progress_bar=False
        )
        return embeddings.tolist()