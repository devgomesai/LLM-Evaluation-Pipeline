import os
from groq import Groq
from ..config import Config
from ..logger import setup_logger
from .cache_manager import CacheManager

logger = setup_logger(__name__)

class GroqClient:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GroqClient, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        try:
            self.client = Groq(api_key=Config.GROQ_API_KEY)
            self.cache = CacheManager() if Config.ENABLE_CACHING else None
            logger.info("Groq client initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize Groq client: {e}")
            raise

    def evaluate(self, prompt: str, model: str = None, temperature: float = 0.0) -> str:
        if model is None:
            model = Config.GROQ_MODEL_RELEVANCE

        if self.cache:
            cached = self.cache.get(prompt)
            if cached:
                logger.debug("Cache hit for prompt.")
                return cached

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=model,
                temperature=temperature,
            )
            response = chat_completion.choices[0].message.content.strip()
            
            if self.cache:
                self.cache.set(prompt, response)
                
            return response
        except Exception as e:
            logger.error(f"Groq API call failed: {e}")
            return ""
