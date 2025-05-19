import pandas as pd
import numpy as np
from strategies.momentum import MomentumStrategy
from backtester.backtest_engine import BacktestEngine

def test_backtest_engine_runs():
    close_prices = np.concatenate([
        np.linspace(10, 10, 20),
        np.linspace(10, 20, 20),
        np.linspace(20, 10, 20)
    ])
    data = pd.DataFrame({
        "close": close_prices
    })

    strategy = MomentumStrategy(short_window=3, long_window=10)
    engine = BacktestEngine(strategy, initial_cash=10000)
    
    _ = engine.run(data)

    trade_log = engine.get_trade_log()
    stats = engine.get_stats()

    assert not trade_log.empty
    assert "pnl" in trade_log.columns
    assert stats["num_trades"] == len(trade_log)
    assert isinstance(stats["total_return"], float)
    assert 0 <= stats["win_rate"] <= 1

def test_backtest_engine_shorting_and_fees():
    # Simulate up/down prices to trigger long and short
    close_prices = np.concatenate([
        np.linspace(10, 20, 20),
        np.linspace(20, 10, 20),
        np.linspace(10, 15, 20)
    ])
    data = pd.DataFrame({"close": close_prices})
    strategy = MomentumStrategy(short_window=3, long_window=10)
    engine = BacktestEngine(strategy, initial_cash=10000, fee_rate=0.001, trade_size=1000)

    _ = engine.run(data)
    trade_log = engine.get_trade_log()
    stats = engine.get_stats()

    assert not trade_log.empty
    assert "pnl" in trade_log.columns
    assert any(trade["position"] == -1 for _,trade in trade_log.iterrows())
    assert stats["num_trades"] >= 2
    assert stats["total_return"] < 1000     # Should reflect trading fees