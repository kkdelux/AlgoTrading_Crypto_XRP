from strategies.momentum import MomentumStrategy
from backtester.backtest_engine import BacktestEngine
from metrics.dashboard import plot_trades_and_equity
from backtester.data_handler import fetch_ohlcv

if __name__ == "__main__":
    # Fetch XRP/USD from Coinbase
    df = fetch_ohlcv(symbol="XRP/USD", timeframe="1h", limit=500, exchange_id="coinbase")

    strategy = MomentumStrategy(short_window=3, long_window=10)
    engine = BacktestEngine(strategy, trade_size=1000, fee_rate=0.001)
    result = engine.run(df)
    trades = engine.get_trade_log()

    plot_trades_and_equity(result, trades)