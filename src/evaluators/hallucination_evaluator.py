from typing import Dict, Any
from .base_evaluator import BaseEvaluator
from ..llm_service import GroqClient, HALLUCINATION_PROMPT
from ..config import Config

class HallucinationEvaluator(BaseEvaluator):
    def __init__(self):
        self.client = GroqClient()

    def evaluate(self, features: Dict[str, Any]) -> Dict[str, Any]:
        claims = features.get('response_sentences', [])
        context_chunks = features.get('context_chunks', [])
        context_text = " ".join(context_chunks) # Simplified context joining

        supported_count = 0
        unsupported_count = 0
        contradicted_count = 0
        
        claim_results = []

        for claim in claims:
            # Basic filtering for very short claims
            if len(claim.split()) < 3:
                continue

            result = self._verify_claim(claim, context_text)
            claim_results.append({'claim': claim, 'status': result})

            if result == 'SUPPORTED':
                supported_count += 1
            elif result == 'UNSUPPORTED':
                unsupported_count += 1
            elif result == 'CONTRADICTED':
                contradicted_count += 1
        
        total_verified = supported_count + unsupported_count + contradicted_count
        hallucination_score = 0.0
        if total_verified > 0:
            hallucination_score = (unsupported_count + contradicted_count) / total_verified

        return {
            'hallucination_score': hallucination_score, # Lower is better
            'accuracy_score': 1.0 - hallucination_score,
            'supported_claims': supported_count,
            'unsupported_claims': unsupported_count,
            'contradicted_claims': contradicted_count,
            'claim_details': claim_results
        }

    def _verify_claim(self, claim: str, context: str) -> str:
        # Optimization: Check for simple keyword overlap first
        # (This is a simplified heuristic, real implementation would be more robust)
        
        prompt = HALLUCINATION_PROMPT.format(claim=claim, context=context[:10000]) # Truncate context if too long
        result = self.client.evaluate(prompt, model=Config.GROQ_MODEL_HALLUCINATION)
        
        if "SUPPORTED" in result:
            return "SUPPORTED"
        elif "CONTRADICTED" in result:
            return "CONTRADICTED"
        else:
            return "UNSUPPORTED"
