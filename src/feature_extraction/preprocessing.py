import re

def preprocess_text(text: str) -> str:
    """Cleans and normalizes text."""
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Basic cleaning (can be expanded)
    return text

def split_sentences(text: str) -> list[str]:
    """Splits text into sentences."""
    # Simple regex for sentence splitting
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    return [s.strip() for s in sentences if s.strip()]
