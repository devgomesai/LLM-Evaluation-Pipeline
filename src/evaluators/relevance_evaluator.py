import re
from typing import Dict, Any
from .base_evaluator import BaseEvaluator
from ..llm_service import GroqClient, RELEVANCE_PROMPT, COMPLETENESS_PROMPT
from ..config import Config

class RelevanceEvaluator(BaseEvaluator):
    def __init__(self):
        self.client = GroqClient()

    def evaluate(self, features: Dict[str, Any]) -> Dict[str, Any]:
        query = features['query']
        response = features['response']

        relevance_score = self._get_llm_score(RELEVANCE_PROMPT, query, response)
        completeness_score = self._get_llm_score(COMPLETENESS_PROMPT, query, response)

        return {
            'relevance_score': relevance_score,
            'completeness_score': completeness_score,
            'weighted_relevance': (relevance_score + completeness_score) / 2
        }

    def _get_llm_score(self, template: str, query: str, response: str) -> float:
        prompt = template.format(query=query, response=response)
        result = self.client.evaluate(prompt, model=Config.GROQ_MODEL_RELEVANCE)
        try:
            # Extract first floating point number
            match = re.search(r"0\.\d+|1\.0|1|0", result)
            if match:
                return float(match.group())
            return 0.0
        except ValueError:
            return 0.0
