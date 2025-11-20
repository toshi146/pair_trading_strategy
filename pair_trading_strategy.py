import yfinance as yf
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint
import matplotlib.pyplot as plt

plt.style.use("default")

print("Starting script...")

# Step 1: Download raw data
tickers = ['KO', 'PEP']
print("Downloading data for:", tickers)

raw = yf.download(tickers, start="2015-01-01", auto_adjust=True)

print("Raw columns:", raw.columns)

# Handle both single- and multi-index columns
if isinstance(raw.columns, pd.MultiIndex):
    # Take the adjusted close prices (now 'Close' after auto_adjust=True)
    data = raw['Close']
else:
    # If columns are just one level, keep only our tickers
    data = raw[tickers]

print("\nPrice data (first 5 rows):")
print(data.head())

print("\nDone.")

# ==============================
# Step 2: Cointegration test
# ==============================
print("\n=== Cointegration test (KO vs PEP) ===")
score, pvalue, _ = coint(data['KO'], data['PEP'])
print(f"Test statistic: {score:.4f}")
print(f"p-value:        {pvalue:.6f}")

# ==============================
# Step 3: Hedge ratio via regression
# ==============================
print("\n=== Hedge ratio (beta) via regression ===")
X = sm.add_constant(data['PEP'])
model = sm.OLS(data['KO'], X).fit()
beta = model.params['PEP']
print(f"Hedge ratio beta (KO ~ beta * PEP): {beta:.4f}")

# ==============================
# Step 4: Build spread and z-score
# ==============================
spread = data['KO'] - beta * data['PEP']
spread_z = (spread - spread.mean()) / spread.std()

print("\nSpread z-score stats:")
print(f"Mean: {spread_z.mean():.4f}")
print(f"Std:  {spread_z.std():.4f}")
print(f"Min:  {spread_z.min():.4f}")
print(f"Max:  {spread_z.max():.4f}")

# ==============================
# Step 5: Simple trading backtest
# ==============================
print("\n=== Running simple backtest ===")
position = 0        # +1 = long spread, -1 = short spread, 0 = flat
returns = []

for i in range(1, len(spread_z)):
    z = spread_z.iloc[i]

    # Entry rules
    if z > 2:
        position = -1  # short spread (short KO, long PEP)
    elif z < -2:
        position = 1   # long spread (long KO, short PEP)

    # Exit rule
    if abs(z) < 0.2:
        position = 0

    # PnL from change in spread
    ret = position * (spread.iloc[i] - spread.iloc[i-1])
    returns.append(ret)

ret_series = pd.Series(returns, index=spread.index[1:])

# Annualized Sharpe (assuming 252 trading days)
sharpe = ret_series.mean() / ret_series.std() * np.sqrt(252)

# Max drawdown
cum = ret_series.cumsum()
running_max = cum.cummax()
drawdown = running_max - cum
max_dd = drawdown.max()

print(f"\nSharpe ratio:     {sharpe:.4f}")
print(f"Max drawdown ($): {max_dd:.4f}")

# Optional: plot equity curve
plt.figure()
cum.plot()
plt.title("Cumulative PnL of Pair Trading Strategy (KO vs PEP)")
plt.xlabel("Date")
plt.ylabel("PnL")
plt.tight_layout()
plt.show()
