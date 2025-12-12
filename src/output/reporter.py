import json
import os
from typing import Dict, Any
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    class Fore:
        GREEN = ""
        YELLOW = ""
        RED = ""
        CYAN = ""
        WHITE = ""
    class Style:
        RESET_ALL = ""
        BRIGHT = ""

from ..logger import setup_logger

logger = setup_logger(__name__)

def print_summary(result: Dict[str, Any]):
    overall = result['overall_score']
    status = result['reliability_status']
    
    color = Fore.GREEN
    if status == "MODERATE":
        color = Fore.YELLOW
    elif status == "UNRELIABLE":
        color = Fore.RED

    print("\n" + "="*50)
    print(f"{Style.BRIGHT}EVALUATION SUMMARY{Style.RESET_ALL}")
    print("="*50)
    print(f"Overall Score:      {color}{overall}{Style.RESET_ALL}")
    print(f"Reliability Status: {color}{status}{Style.RESET_ALL}")
    print("-" * 50)
    
    dims = result['dimensions']
    print(f"Relevance:          {dims['relevance'].get('relevance_score', 0):.2f}")
    print(f"Completeness:       {dims['relevance'].get('completeness_score', 0):.2f}")
    print(f"Accuracy:           {dims['hallucination'].get('accuracy_score', 0):.2f}")
    print(f"Hallucination:      {dims['hallucination'].get('hallucination_score', 0):.2f}")
    print("-" * 50)
    print(f"Est. Cost:          ${dims['efficiency'].get('estimated_cost_usd', 0):.6f}")
    print("="*50 + "\n")

def generate_report(result: Dict[str, Any], output_path: str = "result.json"):
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2)
        logger.info(f"Evaluation report saved to {output_path}")
    except Exception as e:
        logger.error(f"Failed to save report: {e}")
