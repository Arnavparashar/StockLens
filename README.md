📈 StockLens: Interactive Financial Dashboard
StockLens is a fully interactive financial analytics dashboard built to democratize stock market data. Designed for investors, students, and finance enthusiasts, it leverages the power of Python and Streamlit to transform complex market data into actionable insights.

Users can explore historical performance, visualize critical technical indicators, and analyze market trends through dynamic, professional-grade visualizations.

🚀 Launch Live Dashboard
🌟 Key Features
Real-Time Market Data: Instantly fetch live data for any stock symbol (e.g., AAPL, TSLA, RELIANCE.NS) using the yfinance library.

Advanced Technical Analysis:

RSI (Relative Strength Index): Identify overbought or oversold conditions.

Moving Averages: Visualize trends with SMA (Simple) and EMA (Exponential) overlays.

Bollinger Bands: Analyze volatility and potential price breakouts.

Interactive Visualizations: High-performance Plotly candlestick charts allowing for zooming, panning, and detailed data inspection.

Deep Data Dive: Access granular daily data including Open, Close, High, Low, and Volume metrics.

Flexible Timeframes: Toggle seamlessly between 1-month, 3-month, 6-month, and 1-year historical views.

🛠️ Tech Stack
Frontend/Framework: Streamlit

Data Source: yfinance (Yahoo Finance API)

Visualization: Plotly

Data Manipulation: Pandas, NumPy

Language: Python

📂 Project Structure
Plaintext

financial-dashboard/
├── .streamlit/
│   └── config.toml          # Streamlit UI configuration
├── financial_dashboard.py   # Main application entry point
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
💻 Local Installation & Setup
If you wish to run this dashboard locally, follow these steps:

Clone the repository:

Bash

git clone https://github.com/your-username/stocklens.git
cd stocklens
Install dependencies:

Bash

pip install -r requirements.txt
Run the application:

Bash

streamlit run financial_dashboard.py
🔮 Future Roadmap
The following features are planned for future releases:

[ ] Integration of MACD (Moving Average Convergence Divergence) indicators.

[ ] Multi-stock comparison charts for benchmarking performance.

[ ] Export functionality (download charts/reports as CSV or PDF).

[ ] Mobile-responsive layout optimizations.

👨‍💻 About the Creator
Gyanvi Agarwal Final Year, Computer Science and Engineering | VIT

A passionate developer bridging the gap between Data Science and Finance. I specialize in building impactful tech solutions that make complex data accessible and understandable.

📄 License
This project is open-source and available under the MIT License. You are free to use, modify, and distribute it with proper attribution.
