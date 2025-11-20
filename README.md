StockLens — Financial Dashboard

StockLens is a clean and intuitive Streamlit dashboard for exploring stock market performance.
It provides real-time data, interactive charts, and essential technical indicators — designed with a modern, minimal UI.

✨ Highlights

Interactive candlestick charts (Plotly)

Live stock data (yfinance)

Technical indicators:

RSI

SMA

EMA

Multiple time ranges (1M, 3M, 6M, 1Y, YTD)

Clean OHLCV table (Open, High, Low, Close, Volume)

Lightweight single-file Streamlit application

🔗 Live Demo

Run the live app:
https://stocklens-awrx5pgwutdfsjsdwagzyj.streamlit.app/

🧱 Tech Stack
Layer	Tools
Frontend	Streamlit
Visuals	Plotly
Data Source	yfinance
Processing	Pandas, NumPy
Language	Python
📁 Project Structure
financial-dashboard/
│
├── financial_dashboard.py
├── requirements.txt
└── .streamlit/
    └── config.toml

🚀 Run Locally
1. Create virtual environment
python -m venv .venv

2. Activate environment

Windows

.venv\Scripts\activate


macOS / Linux

source .venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

4. Run the app
streamlit run financial_dashboard.py

📌 Roadmap

MACD and Bollinger Bands

Multi-stock comparison

Export charts (CSV, PDF)

Dark/Light theme toggle

Mobile UI improvements

👨‍💻 Developer

Built by Arnav Parashar,
Final-year IT student at VIT Vellore.
Passionate about practical data analytics and clean UI.

📄 License

MIT License — free to use, modify, and distribute.

🚨 IMPORTANT (you MUST do this or it will break AGAIN)
✔ Open README in VS Code
✔ At bottom-right: click CRLF → LF
✔ Save file
✔ Then run:
git add README.md
git commit -m "Fix README formatting"
git push --force
