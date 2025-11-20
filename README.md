Pair Trading Strategy : KOvsPEP

This project builds and tests a simple statistical-arbitrage strategy using Coca-Cola (KO) and Pepsi (PEP). 
It downloads real historical data, checks whether the two stocks move together long-term, builds a tradable spread, and runs a basic backtest.

Tools & Libraries :
Python
NumPy
Pandas
Statsmodels
SciPy
Matplotlib
yfinance

All dependencies are listed in requirements.txt.

How it Works
1. Data Download

Pulls KO and PEP daily prices from Yahoo Finance.

Uses clean, aligned closing-price data.

2. Cointegration Test

Uses the Engle-Granger test to check whether KO and PEP have a stable long-run relationship.

Cointegration is a core requirement for pair trading.

3. Hedge Ratio

Simple regression:

KO ~ beta * PEP


The slope (beta) becomes the hedge ratio that defines the spread.

4. Spread & Z-Score

Build the spread:

spread = KO – beta * PEP


Then convert it into a rolling z-score to detect when the spread is unusually wide or unusually tight.

5. Backtest Rules

The trading logic is straightforward:

Z < –2 → Go long the spread

Z > +2 → Go short the spread

–0.2 < Z < 0.2 → Close positions

The script tracks daily PnL, cumulative returns, Sharpe ratio, and drawdowns, and plots performance.

🧠 Why the PnL Looks Flat (and Then Moves)

The PnL is flat for years because KO and PEP almost never drift far enough apart to hit the ±2σ entry thresholds.

No threshold hit = no trades = flat line.

Later (around 2024–2025), volatility picks up and the spread finally starts firing signals. That’s when trades occur, and the PnL suddenly moves — sometimes sharply.

This is completely normal for threshold-based mean-reversion strategies:

quiet periods → sudden activity when the spread finally breaks out.

📊 What the Script Outputs

Cointegration statistic & p-value

Hedge ratio

Spread summary stats

Sharpe ratio

Max drawdown

Sample of price data

A plot of cumulative PnL

📂 Project Structure
pair_trading_strategy.py
requirements.txt
README.md
.venv/

🏃 How to Run
1. Activate the virtual environment
cd ~/Downloads/CS
source .venv/bin/activate

2. Run the script
python pair_trading_strategy.py