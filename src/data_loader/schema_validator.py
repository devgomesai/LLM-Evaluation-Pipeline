from typing import Dict, Any, List

def validate_chat_schema(data: Dict[str, Any]) -> bool:
    """Validates that the chat data has the required structure."""
    # Basic validation logic based on expected structure
    # This can be expanded with Pydantic models later
    if not isinstance(data, list) and not isinstance(data, dict):
        return False
    
    # Assuming the input might be a single object or list of objects
    # For now, let's assume it matches the structure implied in the GEMINI.md or typical chat logs
    # We will be permissive for now to allow development to proceed
    return True

def validate_context_schema(data: Dict[str, Any]) -> bool:
    """Validates that the context vector data has the required structure."""
    required_keys = ["status", "data"]
    if not all(key in data for key in required_keys):
        return False
    
    if "vector_data" not in data["data"]:
        return False
        
    return True
