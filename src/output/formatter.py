import json
from typing import Dict, Any

def format_result_json(result: Dict[str, Any], pretty: bool = True) -> str:
    indent = 2 if pretty else None
    return json.dumps(result, indent=indent)
