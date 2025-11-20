📈 StockLens: Interactive Financial Dashboard

StockLens is a fully interactive financial analytics dashboard built to make stock market insights accessible to everyone.
Designed for investors, students, and finance enthusiasts, it transforms complex market data into clear, actionable visual insights using Streamlit, Plotly, and yfinance.

Users can explore historical performance, analyze technical indicators, and identify market trends through smooth, modern, professional-grade visualizations.

🚀 Launch Live Dashboard

https://stocklens-awrx5pgwutdfsjsdwagzyj.streamlit.app/

🌟 Key Features
Real-Time Market Data

Fetch instantly updated market data for any stock symbol (AAPL, TSLA, INFY, RELIANCE.NS, etc.) via the yfinance API.

Advanced Technical Analysis

RSI (Relative Strength Index)
Helps identify overbought/oversold zones.

Moving Averages

SMA (Simple Moving Average)

EMA (Exponential Moving Average)
Useful for understanding price trends and smoothing volatility.

(Upcoming) Bollinger Bands, MACD, and more indicators.

Interactive Visualizations

High-quality Plotly candlestick charts

Zooming, panning, hover information

Smooth user interaction with dynamic chart updates

Deep Data Dive

Access daily Open, Close, High, Low, and Volume metrics in a clean and readable view.

Flexible Timeframes

View and compare historical performance across:

1 Month

3 Months

6 Months

1 Year

🛠️ Tech Stack

Frontend / Framework: Streamlit
Data Source: yfinance (Yahoo Finance API)
Visualization: Plotly
Data Manipulation: Pandas, NumPy
Language: Python

📂 Project Structure
financial-dashboard/
├── .streamlit/
│   └── config.toml            # Streamlit theme and UI configuration
├── financial_dashboard.py     # Main Streamlit dashboard
├── requirements.txt           # Python package dependencies
└── README.md                  # Project documentation

💻 Local Installation & Setup

Follow the steps below to run this dashboard on your system:

1️⃣ Clone the repository
git clone https://github.com/Arnavparashar/StockLens.git
cd StockLens

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Run the application
streamlit run financial_dashboard.py

🔮 Future Roadmap

 MACD (Moving Average Convergence Divergence) indicator

 Bollinger Bands

 Multi-stock comparison & benchmarking

 Export charts/reports (CSV or PDF)

 Mobile-responsive layout improvements

 Light/Dark theme toggle

👨‍💻 About the Developer

Arnav Parashar
Final-year IT student at VIT Vellore

Focused on:

Data Analytics

Financial Technology

Streamlit Dashboards

Clean and intuitive data visualization





📄 License

This project is open-source and available under the MIT License.
Feel free to use, modify, and distribute it with proper attribution.
