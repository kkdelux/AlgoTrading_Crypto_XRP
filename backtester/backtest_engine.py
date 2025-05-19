import pandas as pd
from strategies.base_strategy import BaseStrategy

class BacktestEngine:
    def __init__(self,
            strategy: BaseStrategy,
            initial_cash: float = 10000,
            fee_rate: float = 0.001,
            trade_size: float = 1000
        ):
        self.strategy = strategy
        self.initial_cash = initial_cash
        self.fee_rate = fee_rate
        self.trade_size = trade_size
        
        self.reset()

    def reset(self):
        self.cash = self.initial_cash
        self.position = 0   # 0 = flat, 1 = long, -1 = short
        self.entry_price = 0
        self.entry_index = None
        self.trades = []
        self.equity_curve = []

    def run(self, data: pd.DataFrame) -> pd.DataFrame:
        self.reset()
        data = data.copy()
        signals = self.strategy.generate_signals(data)

        for i in range(1, len(data)):
            price = data['close'].iloc[i]
            prev_signal = signals.iloc[i - 1]
            signal = signals.iloc[i]

            # Entry Logic
            if self.position == 0 and signal in [1, -1]:
                self.position =  signal
                self.entry_price = price
                self.entry_index = i
                self.trades.append({
                    "type": "BUY" if signal == 1 else "SELL_SHORT",
                    "entry_price": price,
                    "entry_index": i,
                    "position": signal,
                })

                self.cash -= self.trade_size * self.fee_rate  # Entry fee

            # Exit Logic
            elif self.position != 0 and (signal == 0 or signal == -self.position):
                direction = self.position
                exit_price = price
                pnl = (exit_price - self.entry_price) * direction * (self.trade_size / self.entry_price)
                self.cash += pnl
                self.cash -= self.trade_size * self.fee_rate  # Exit fee

                self.trades[-1].update({
                    "exit_price": exit_price,
                    "exit_index": i,
                    "pnl": pnl,
                    "return_pct": pnl / self.trade_size,
                    "duration": i - self.entry_index
                })
                self.position = 0
                self.entry_price = 0
                self.entry_index = None
            
            # Track equity
            floating_pnl = 0
            if self.position != 0:
                floating_pnl = (price - self.entry_price) * self.position * (self.trade_size / self.entry_price)
            equity = self.cash + floating_pnl
            self.equity_curve.append(equity)

        data = data.iloc[1:].copy()
        data["equity"] = self.equity_curve
        return data
    
    def get_trade_log(self) -> pd.DataFrame:
        return pd.DataFrame(self.trades)
    
    def get_stats(self) -> dict:
        df = self.get_trade_log()
        if df.empty:
            return {"total__return": 0, "num_trades": 0}
        
        total_return = df["pnl"].sum()
        win_rate = (df["pnl"] > 0).mean()
        avg_return = df["pnl"].mean()
        return {
            "total_return": total_return,
            "num_trades": len(df),
            "win_rate": win_rate,
            "avg_return": avg_return
        }