import pandas as pd
from strategies.base_strategy import BaseStrategy

class MomentumStrategy(BaseStrategy):
    def __init__(self, short_window=5, long_window=20):
        super().__init__()
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        short_ma = data['close'].rolling(window=self.short_window).mean()
        long_ma = data['close'].rolling(window=self.long_window).mean()
        
        signal = pd.Series(0, index=data.index)
        signal[short_ma > long_ma] = 1
        signal[short_ma < long_ma] = -1
        return signal