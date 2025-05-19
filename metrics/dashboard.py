import matplotlib.pyplot as plt
import pandas as pd

def plot_trades_and_equity(price_data: pd.DataFrame, trades: pd.DataFrame):
    if "equity" not in price_data.columns:
        raise ValueError("Equity column not found.")

    # Ensure index is datetime
    if not pd.api.types.is_datetime64_any_dtype(price_data.index):
        raise ValueError("Index must be datetime for time-based plotting.")

    fig, axs = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

    # --- Price Plot with Trade Markers ---
    axs[0].plot(price_data.index, price_data["close"], label="Close", color="black")

    for _, trade in trades.iterrows():
        entry_idx = trade["entry_index"]
        entry_price = trade["entry_price"]
        position = trade["position"]

        try:
            entry_time = price_data.index[entry_idx]
            axs[0].plot(entry_time, entry_price,
                        "g^" if position == 1 else "rv",
                        label="Entry" if _ == 0 else "", markersize=10)
            if "exit_index" in trade and pd.notnull(trade["exit_index"]):
                exit_time = price_data.index[int(trade["exit_index"])]
                axs[0].plot(exit_time, trade["exit_price"], "kx", label="Exit" if _ == 0 else "", markersize=10)
        except IndexError:
            continue

    axs[0].set_title("Price with Trade Markers")
    axs[0].legend(loc="upper left")
    axs[0].grid(True)

    # --- Equity Curve with Drawdown ---
    equity = price_data["equity"]
    peak = equity.cummax()
    drawdown = equity - peak

    axs[1].plot(equity.index, equity, label="Equity", color="blue", linewidth=2)
    axs[1].fill_between(equity.index, equity, peak, where=(equity < peak), color="red", alpha=0.3, label="Drawdown")
    axs[1].set_title("Equity Curve with Drawdown")
    axs[1].legend()
    axs[1].grid(True)

    plt.xlabel("Time")
    plt.tight_layout()
    plt.show()
