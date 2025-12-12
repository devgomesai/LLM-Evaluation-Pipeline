from typing import Dict, Any
from ..config import Config

def aggregate_results(
    relevance_metrics: Dict[str, Any],
    hallucination_metrics: Dict[str, Any],
    latency_cost_metrics: Dict[str, Any]
) -> Dict[str, Any]:
    
    # Weights (can be moved to config)
    w_relevance = 0.25
    w_completeness = 0.25
    w_hallucination = 0.40
    w_cost_latency = 0.10 # Combined
    
    rel_score = relevance_metrics.get('relevance_score', 0)
    comp_score = relevance_metrics.get('completeness_score', 0)
    acc_score = hallucination_metrics.get('accuracy_score', 0)
    
    # Latency/Cost are not typically 0-1 scores where higher is better in the same way,
    # so we might omit them from the weighted score or normalize them.
    # For now, we'll exclude them from the "quality" score.
    
    weighted_score = (
        (rel_score * w_relevance) +
        (comp_score * w_completeness) +
        (acc_score * w_hallucination)
    ) / (w_relevance + w_completeness + w_hallucination)

    # Reliability Classification
    if weighted_score >= 0.8:
        reliability = "RELIABLE"
    elif weighted_score >= 0.6:
        reliability = "MODERATE"
    else:
        reliability = "UNRELIABLE"

    return {
        'overall_score': round(weighted_score, 4),
        'reliability_status': reliability,
        'dimensions': {
            'relevance': relevance_metrics,
            'hallucination': hallucination_metrics,
            'efficiency': latency_cost_metrics
        }
    }
