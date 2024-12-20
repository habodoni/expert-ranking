from sentence_transformers import SentenceTransformer

class EmbeddingEngine:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)

    def embed(self, text: str):
        return self.model.encode(text, convert_to_tensor=True)

    def batch_embed_texts(self, texts):
        return self.model.encode(texts, convert_to_tensor=True)
