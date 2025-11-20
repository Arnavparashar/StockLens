StockLens — Financial Dashboard

StockLens is a clean and intuitive Streamlit dashboard for exploring stock market performance.
It provides real-time data, interactive charts, and essential technical indicators — designed with a modern, minimal UI.

✨ Highlights

Interactive candlestick charts powered by Plotly

Live stock data fetched via yfinance

Built-in technical indicators:

RSI

SMA

EMA

Multiple time range filters (1M, 3M, 6M, 1Y, YTD)

Clean daily OHLCV table (Open, High, Low, Close, Volume)

Lightweight single-file Streamlit application

🔗 Live Demo

Run the live app here:
https://stocklens-awrx5pgwutdfsjsdwagzyj.streamlit.app/

🧱 Tech Stack
Layer	Tools
Frontend	Streamlit
Visualization	Plotly
Data Source	yfinance
Data Processing	Pandas, NumPy
Language	Python
📁 Project Structure
financial-dashboard/
│
├── financial_dashboard.py     # Main Streamlit application
├── requirements.txt           # Required dependencies
└── .streamlit/
    └── config.toml            # Streamlit configuration

🚀 Run Locally
python -m venv .venv
# activate environment
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
streamlit run financial_dashboard.py

📌 Roadmap

Add MACD and Bollinger Bands

Compare multiple tickers in one chart

Export charts/reports (CSV, PDF)

Dark/Light theme toggle

Mobile layout improvements

👨‍💻 Developer

Built by Arnav Parashar
Final-year IT student at VIT Vellore, focused on clean UI and practical data applications.

📄 License

MIT License — free to use, modify, and distribute.