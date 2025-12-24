from app.logging import logger
import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

class LLMClient:
    def generate(self, prompt:str) -> str:
        logger.info(f"Generating response for prompt: {prompt}")
        payload = {
            "model":MODEL,
            "prompt":prompt,
            "stream":False
        }

        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        logger.info(f"Response: {response.json()}")
        response.raise_for_status()

        return response.json()["response"]

        