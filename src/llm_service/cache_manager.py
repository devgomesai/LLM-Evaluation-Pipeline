import json
import os
import hashlib
from typing import Optional

class CacheManager:
    def __init__(self, cache_dir=".cache"):
        self.cache_dir = cache_dir
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

    def _get_key(self, prompt: str) -> str:
        return hashlib.md5(prompt.encode('utf-8')).hexdigest()

    def get(self, prompt: str) -> Optional[str]:
        key = self._get_key(prompt)
        path = os.path.join(self.cache_dir, f"{key}.json")
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f).get('response')
        return None

    def set(self, prompt: str, response: str):
        key = self._get_key(prompt)
        path = os.path.join(self.cache_dir, f"{key}.json")
        with open(path, 'w', encoding='utf-8') as f:
            json.dump({'prompt': prompt, 'response': response}, f)
