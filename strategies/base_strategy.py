from abc import ABC, abstractmethod
import pandas as pd

class BaseStrategy(ABC):
    """
    Abstract base class for all trading strategies.
    """

    def __init__(self):
        self.position = 0   # 1 for long, -1 for short, 0 for flat

    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """
        Generate trading signals based on the provided data.

        Args:
            data (pd.DataFrame): Historical OHLCV data.
        
        Returns:
            pd.Series: Signal for each row in data (1 = buy, -1 = sell, 0 = hold).
        """
        pass

    def reset(self):
        """
        Reset internal state between runs.
        """
        self.position = 0