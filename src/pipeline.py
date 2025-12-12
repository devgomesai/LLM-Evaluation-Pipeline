import time
from typing import Dict, Any

from .data_loader import load_chat_data, load_context_data
from .feature_extraction import extract_features
from .evaluators import RelevanceEvaluator, HallucinationEvaluator, LatencyCostEvaluator
from .aggregation import aggregate_results
from .output import print_summary, generate_report
from .logger import setup_logger

logger = setup_logger(__name__)

class EvaluationPipeline:
    def __init__(self):
        self.relevance_evaluator = RelevanceEvaluator()
        self.hallucination_evaluator = HallucinationEvaluator()
        self.latency_evaluator = LatencyCostEvaluator()

    def run(self, chat_file: str, context_file: str, output_file: str = "result.json"):
        logger.info("Starting Evaluation Pipeline...")
        start_time = time.time()

        # 1. Load Data
        logger.info("Loading data...")
        chat_data = load_chat_data(chat_file)
        context_data = load_context_data(context_file)

        # 2. Extract Features
        logger.info("Extracting features...")
        features = extract_features(chat_data, context_data)

        # 3. Evaluate Dimensions (could be parallelized)
        logger.info("Evaluating Relevance & Completeness...")
        relevance_metrics = self.relevance_evaluator.evaluate(features)
        
        logger.info("Evaluating Hallucination & Accuracy...")
        hallucination_metrics = self.hallucination_evaluator.evaluate(features)
        
        logger.info("Calculating Latency & Costs...")
        latency_metrics = self.latency_evaluator.evaluate(features)

        # 4. Aggregate Results
        logger.info("Aggregating results...")
        final_result = aggregate_results(
            relevance_metrics,
            hallucination_metrics,
            latency_metrics
        )
        
        # Add metadata
        final_result['metadata'] = {
            'execution_time_sec': round(time.time() - start_time, 2),
            'chat_source': chat_file,
            'context_source': context_file
        }
        
        # Add original query/response for context in report
        final_result['input_data'] = {
            'query': features['query'],
            'response': features['response']
        }

        # 5. Output
        print_summary(final_result)
        generate_report(final_result, output_file)
        
        logger.info("Pipeline execution complete.")
        return final_result
