import json
import os
from typing import Dict, Any
from ..logger import setup_logger
from .schema_validator import validate_chat_schema, validate_context_schema

logger = setup_logger(__name__)

def load_json_file(file_path: str) -> Dict[str, Any]:
    """Loads a JSON file from the given path."""
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        logger.error(f"Error loading JSON file {file_path}: {e}")
        raise

def load_chat_data(file_path: str) -> Dict[str, Any]:
    """Loads and validates chat data."""
    data = load_json_file(file_path)
    if not validate_chat_schema(data):
        logger.warning(f"Chat data in {file_path} might not match expected schema.")
    return data

def load_context_data(file_path: str) -> Dict[str, Any]:
    """Loads and validates context data."""
    data = load_json_file(file_path)
    if not validate_context_schema(data):
        logger.warning(f"Context data in {file_path} might not match expected schema.")
    
    # Extract relevant context fields as per GEMINI.md
    context = {
        'vectors': data['data'].get('vector_data', []),
        'retrieval_scores': [v['score'] for v in data['data'].get('sources', {}).get('vectors_info', [])],
        'total_context_tokens': sum(v.get('tokens', 0) for v in data['data'].get('vector_data', [])),
        'sources_used': data['data'].get('sources', {}).get('vectors_used', [])
    }
    return context
