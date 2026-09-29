from abc import ABC, abstractmethod
from typing import Tuple, Dict, Any

class BaseParser(ABC):
    """
    Abstract Base Class interface for modular forensic evidence parsers.
    Every parser implementation must return (parsed_text: str, metadata: Dict[str, Any]).
    """
    @abstractmethod
    def parse(self, file_path: str) -> Tuple[str, Dict[str, Any]]:
        pass
