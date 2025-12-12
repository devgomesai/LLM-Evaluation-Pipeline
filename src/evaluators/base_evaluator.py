from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseEvaluator(ABC):
    @abstractmethod
    def evaluate(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate specific dimension based on features.
        Returns a dictionary of metrics.
        """
        pass
