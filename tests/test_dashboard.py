import pandas as pd
import numpy as np
from metrics.dashboard import plot_equity_curve

def test_plot_equity_curve():
    df = pd.DataFrame({
        "equity": np.linspace(10000, 12000, 100)
    })
    try:
        plot_equity_curve(df)
    except Exception as e:
        assert False, f"Plot failed: {e}"