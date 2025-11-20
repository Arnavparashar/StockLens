StockLens — Financial Dashboard

StockLens is a simple, clean Streamlit dashboard for exploring stock prices with live data and technical indicators.
It is built for clarity, speed and ease of use.

Features

Live stock price lookup

Interactive candlestick chart

RSI, SMA, EMA indicators

Multiple time ranges (1M, 3M, 6M, 1Y, YTD)

OHLCV daily data table

Lightweight single-file app

Live Demo

https://stocklens-awrx5pgwutdfsjsdwagzyj.streamlit.app/

Tech Stack

Python

Streamlit

Plotly

yfinance

Pandas

NumPy

Project Structure
financial-dashboard/
  financial_dashboard.py
  requirements.txt
  .streamlit/
    config.toml

Run Locally
python -m venv .venv


Windows:

.venv\Scripts\activate


macOS / Linux:

source .venv/bin/activate


Install packages:

pip install -r requirements.txt


Run:

streamlit run financial_dashboard.py

Developer

Built by Arnav Parashar
Final-year IT student at VIT Vellore.

License

MIT License
