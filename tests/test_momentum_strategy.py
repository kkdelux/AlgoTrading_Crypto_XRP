import pandas as pd
import numpy as np
from strategies.momentum import MomentumStrategy

def test_momentum_strategy():
    # Create test data
    close_prices = np.concatenate([np.ones(20)*10, np.ones(20)*20])
    data = pd.DataFrame({
        'close': close_prices
    })

    strategy = MomentumStrategy(short_window=3, long_window=10)
    signals = strategy.generate_signals(data)

    # The beginning will have NaNs due to rolling
    valid_signals = signals.dropna()
    assert isinstance(signals, pd.Series)
    assert (valid_signals.isin([1, 0, -1]).all())

    # After prices go from 10 to 20, we expect a buy signal to appear
    assert 1 in signals[-20:].values