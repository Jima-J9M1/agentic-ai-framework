import time
import faiss
from sentence_transformers import SentenceTransformer

from app.logging import logger


class VectorMemory:
    def __init__(self, ttl_seconds:int=3600):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = faiss.IndexFlatL2(self.model.get_sentence_embedding_dimension())
        self.texts = []
        self.timestamps = []
        self.ttl = ttl_seconds
    
    def _cleanup(self):
        now = time.time()

        valid = [
            i for i, timestamp in enumerate(self.timestamps)
            if now - timestamp < self.ttl
        ]

        if len(valid) == len(self.texts):
            return


        self.texts = [self.texts[i] for i in valid]
        self.timestamps = [self.timestamps[i] for i in valid]

        self.index.reset()

        if self.texts:
            embedding = self.model.encode(self.texts)
            self.index.add(embedding)




        
    def add(self, text:str):
        logger.info(f"Adding text to vector memory: {text}")
        self._cleanup()
        embedding = self.model.encode([text])
        self.index.add(embedding)
        self.texts.append(text)
        self.timestamps.append(time.time())

    def search(self, query:str, k:int=5):
        self._cleanup()
        print(f"Length of texts: {len(self.texts)}")
        if len(self.texts) == 0:
            return []

        embedding = self.model.encode([query])

        _, indices = self.index.search(embedding, k)

        return [self.texts[i] for i in indices[0] if i < len(self.texts)]