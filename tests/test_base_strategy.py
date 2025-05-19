import pytest
import pandas as pd
from strategies.base_strategy import BaseStrategy

class DummyStrategy(BaseStrategy):
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        return pd.Series([0] * len(data), index=data.index)
    
def test_cannot_instantiate_base_strategy():
    with pytest.raises(TypeError):
        BaseStrategy()

def test_dummy_strategy_generates_signals():
    data = pd.DataFrame({
        'open': [1, 2, 3],
        'high': [1.1, 2.1, 3.1],
        'low': [0.9, 1.9, 2.9],
        'close': [1, 2, 3],
        'volume': [100, 200, 300]
    })
    strategy = DummyStrategy()
    signals = strategy.generate_signals(data)
    assert isinstance(signals, pd.Series)
    assert (signals == 0).all()