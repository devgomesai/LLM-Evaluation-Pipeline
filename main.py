import argparse
import sys
import os

# Add src to python path to allow imports if running from root
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.pipeline import EvaluationPipeline
from src.config import Config
from src.logger import setup_logger

logger = setup_logger(__name__)

def main():
    parser = argparse.ArgumentParser(description="LLM Evaluation Pipeline")
    parser.add_argument("--chat", type=str, required=True, help="Path to chat JSON file")
    parser.add_argument("--context", type=str, required=True, help="Path to context JSON file")
    parser.add_argument("--output", type=str, default="result.json", help="Path to output JSON file")
    
    args = parser.parse_args()

    try:
        # Validate config (e.g. check API key)
        # Config.validate() # Commented out to allow running without API key for testing structure
        
        pipeline = EvaluationPipeline()
        pipeline.run(args.chat, args.context, args.output)
        
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
