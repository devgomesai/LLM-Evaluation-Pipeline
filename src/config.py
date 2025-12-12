import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(".env")

class Config:
    # Groq API Configuration
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL_RELEVANCE = os.getenv("GROQ_MODEL_RELEVANCE", "llama-3.3-70b-versatile")
    GROQ_MODEL_HALLUCINATION = os.getenv("GROQ_MODEL_HALLUCINATION", "llama-3.3-70b-versatile")

    # Evaluation Thresholds
    RELEVANCE_THRESHOLD = float(os.getenv("RELEVANCE_THRESHOLD", "0.7"))
    COMPLETENESS_THRESHOLD = float(os.getenv("COMPLETENESS_THRESHOLD", "0.7"))
    HALLUCINATION_THRESHOLD = float(os.getenv("HALLUCINATION_THRESHOLD", "0.2"))
    OVERALL_THRESHOLD = float(os.getenv("OVERALL_THRESHOLD", "0.7"))

    # Optimization
    ENABLE_CACHING = os.getenv("ENABLE_CACHING", "true").lower() == "true"
    CACHE_SIZE = int(os.getenv("CACHE_SIZE", "1000"))
    BATCH_SIZE = int(os.getenv("BATCH_SIZE", "10"))
    SAMPLING_RATE = float(os.getenv("SAMPLING_RATE", "1.0"))

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "evaluation.log")

    @staticmethod
    def validate():
        if not Config.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY environment variable is not set.")
