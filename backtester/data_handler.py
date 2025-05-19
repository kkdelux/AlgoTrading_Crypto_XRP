import ccxt
import pandas as pd
import time

def fetch_ohlcv(symbol="XRP/USD", timeframe="1h", limit=500, exchange_id="coinbase") -> pd.DataFrame:
    exchange_class = getattr(ccxt, exchange_id)
    exchange = exchange_class()

    # Load markets to ensure symbols are standardized
    markets = exchange.load_markets()
    if symbol not in markets:
        raise ValueError(f"{symbol} not found on {exchange_id}")
    
    if not exchange.has['fetchOHLCV']:
        raise ValueError(f"{exchange_id} does not support OHLCV data")
    
    # Use Binance's supported timeframe and market
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms')
    df.set_index("timestamp", inplace=True)
    return df