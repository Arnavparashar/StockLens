# financial_dashboard.py

import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

# Set page config (must be first Streamlit call)
st.set_page_config(
    page_title="StockLens",
    page_icon="app-icon.png",  # or use "📈" or a path to a .png file: "app-icon.png"
    layout="wide"
)


# Small UI polish: custom CSS and compact header
st.markdown(
    """
    <style>
    /* Page background and font */
    .stApp { background-color: #0b1020; }
    .app-title {font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #e6eef8; font-size:34px; font-weight:700; margin:0 0 2px 0}
    .app-sub {color:#9aa4b2; margin:0 0 16px 0; font-size:14px}
    .stSidebar .sidebar-content {background-color: #071026}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="app-title">StockLens</div><div class="app-sub">A compact visual dashboard for stock price analysis.</div>', unsafe_allow_html=True)

# Sidebar inputs
st.sidebar.markdown("## Controls")
st.sidebar.markdown("Adjust ticker, date range and indicators below.")

default_tickers = ['AAPL', 'TSLA', 'GOOGL', 'MSFT', 'AMZN', 'META']
ticker = st.sidebar.selectbox("Choose a Stock", default_tickers)
start_date = st.sidebar.date_input("Start Date", value=datetime.today() - timedelta(days=180))
end_date = st.sidebar.date_input("End Date", value=datetime.today())
ma_window = st.sidebar.slider("Moving Average Window", min_value=5, max_value=60, value=20)
rsi_period = st.sidebar.slider("RSI Period", min_value=5, max_value=30, value=14)

# Fetch data
@st.cache_data
def get_data(ticker, start, end):
    df = yf.download(ticker, start=start, end=end)
    # yfinance may return a Series for single-row results; normalize to DataFrame
    if df is None:
        return pd.DataFrame()
    if isinstance(df, pd.Series):
        try:
            df = df.to_frame().T
        except Exception:
            df = pd.DataFrame([df])
    return df

def calculate_moving_average(df, window):
    df["MA"] = df["Close"].rolling(window=window).mean()
    return df

def calculate_rsi(df, period=14):
    delta = df["Close"].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    df["RSI"] = rsi
    return df

def plot_price(df, ticker):
    # Use candlestick for price when OHLC exists; fallback to line if not
    fig = go.Figure()
    if df is None or df.empty or "Close" not in df.columns:
        fig.update_layout(
            template="plotly_dark",
            height=360,
            annotations=[dict(text="No price data available for the selected range.", xref="paper", yref="paper", showarrow=False, x=0.5, y=0.5, font=dict(size=14))]
        )
        return fig

    data = df.copy()
    try:
        data.index = pd.to_datetime(data.index)
    except Exception:
        pass
    data = data.sort_index()

    # Prefer candlestick if OHLC present
    has_ohlc = all(c in data.columns for c in ("Open", "High", "Low", "Close"))

    if has_ohlc:
        fig.add_trace(go.Candlestick(
            x=data.index,
            open=data["Open"].astype(float),
            high=data["High"].astype(float),
            low=data["Low"].astype(float),
            close=data["Close"].astype(float),
            name="OHLC",
            increasing_line_color="#00BFFF",
            decreasing_line_color="#ff4d4d",
            showlegend=False
        ))
    else:
        y = data["Close"].astype(float)
        mode_primary = "lines+markers" if len(y) < 10 else "lines"
        fig.add_trace(go.Scatter(
            x=data.index,
            y=y,
            mode=mode_primary,
            name="Close",
            line=dict(color="#00BFFF", width=2),
            marker=dict(size=6),
            hovertemplate="%{x|%b %d, %Y}<br><b>Close:</b> $%{y:.2f}<extra></extra>"
        ))

    # overlay MA as a clean line
    if "MA" in data.columns and data["MA"].dropna().any():
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data["MA"].astype(float),
            mode="lines",
            name=f"{ma_window}-Day MA",
            line=dict(color="#FF7F50", dash="dot", width=2),
            hovertemplate="%{x|%b %d, %Y}<br><b>MA:</b> $%{y:.2f}<extra></extra>"
        ))

    # Add range selector and modern layout
    fig.update_layout(
        title_text="",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        template="plotly_dark",
        height=540,
        font=dict(size=13),
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=3, label="3m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(visible=False),
            type="date"
        )
    )

    fig.update_yaxes(tickprefix="$", separatethousands=True)
    fig.update_xaxes(showgrid=False)
    return fig

def plot_volume(df, ticker):
    # Render volume as a professional bar chart with clean date ticks and formatted y-axis
    fig = go.Figure()
    if df is None or df.empty or "Volume" not in df.columns:
        fig.update_layout(template="plotly_dark", height=220, annotations=[dict(text="No volume data", xref="paper", yref="paper", showarrow=False, x=0.5, y=0.5)])
        return fig

    data = df.copy()
    # normalize index to midnight (remove stray time components) and sort
    try:
        data.index = pd.to_datetime(data.index).normalize()
    except Exception:
        try:
            data.index = pd.to_datetime(data.index)
        except Exception:
            pass
    data = data.sort_index()

    vol = data["Volume"].astype(float)

    # Use bars for volume — more standard and easier to read
    fig.add_trace(go.Bar(
        x=data.index,
        y=vol,
        marker_color="#20c997",
        opacity=0.85,
        name="Volume",
        hovertemplate="%{x|%b %d, %Y}<br><b>Volume:</b> %{y:,}<extra></extra>"
    ))

    # Layout: monthly ticks, limited number of ticks, no grid clutter
    fig.update_layout(
        title=f"{ticker} Daily Volume",
        xaxis_title="Date",
        yaxis_title="Volume",
        template="plotly_dark",
        height=300,
        font=dict(size=12),
        hovermode="x unified",
        showlegend=False,
        margin=dict(l=60, r=20, t=50, b=60),
        xaxis=dict(type="date", tickformat="%b %Y", nticks=6)
    )

    # Format the y-axis with thousands separators
    fig.update_yaxes(tickformat=",.0f", separatethousands=True)
    fig.update_xaxes(showgrid=False)
    return fig

def plot_rsi(df, ticker):
    # Use a filled area for RSI to make momentum obvious
    fig = go.Figure()
    if df is None or df.empty or "RSI" not in df.columns:
        fig.update_layout(template="plotly_dark", height=220, annotations=[dict(text="No RSI data", xref="paper", yref="paper", showarrow=False, x=0.5, y=0.5)])
        return fig

    data = df.copy()
    try:
        data.index = pd.to_datetime(data.index)
    except Exception:
        pass
    data = data.sort_index()

    rsi_y = data["RSI"].astype(float)
    mode_rsi = "lines" if len(rsi_y) >= 10 else "lines+markers"

    fig.add_trace(go.Scatter(
        x=data.index,
        y=rsi_y,
        mode=mode_rsi,
        name="RSI",
        line=dict(color="#FFD700", width=2),
        fill="tozeroy",
        fillcolor="rgba(255,215,0,0.08)",
        hovertemplate="%{x|%b %d, %Y}<br><b>RSI:</b> %{y:.1f}<extra></extra>"
    ))

    # threshold lines
    fig.add_hline(y=70, line_dash="dash", line_color="red", opacity=0.6)
    fig.add_hline(y=30, line_dash="dash", line_color="green", opacity=0.6)

    fig.update_layout(
        title=f"{ticker} RSI (Relative Strength Index)",
        xaxis_title="Date",
        yaxis_title="RSI",
        yaxis_range=[0, 100],
        template="plotly_dark",
        height=300,
        font=dict(size=12),
        hovermode="x unified",
        showlegend=False
    )

    fig.update_xaxes(showgrid=False)
    return fig


def plot_price_with_volume(df, ticker):
    """Combined candlestick/line price chart with a volume subplot (shared x-axis)."""
    if df is None or df.empty or "Close" not in df.columns:
        fig = go.Figure()
        fig.update_layout(template="plotly_dark", height=420, annotations=[dict(text="No data available", xref="paper", yref="paper", showarrow=False, x=0.5, y=0.5)])
        return fig

    data = df.copy()
    try:
        data.index = pd.to_datetime(data.index).normalize()
    except Exception:
        try:
            data.index = pd.to_datetime(data.index)
        except Exception:
            pass
    data = data.sort_index()

    has_ohlc = all(c in data.columns for c in ("Open", "High", "Low", "Close"))

    # create subplots: price (larger) and volume (smaller)
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.7, 0.25], vertical_spacing=0.03)

    if has_ohlc:
        fig.add_trace(go.Candlestick(
            x=data.index,
            open=data["Open"].astype(float),
            high=data["High"].astype(float),
            low=data["Low"].astype(float),
            close=data["Close"].astype(float),
            increasing_line_color="#00BFFF",
            decreasing_line_color="#ff4d4d",
            name="Price"
        ), row=1, col=1)
    else:
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data["Close"].astype(float),
            mode="lines",
            line=dict(color="#00BFFF", width=2),
            name="Close"
        ), row=1, col=1)

    # moving average overlay
    if "MA" in data.columns and data["MA"].dropna().any():
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data["MA"].astype(float),
            mode="lines",
            line=dict(color="#FF7F50", dash="dot", width=2),
            name=f"{ma_window}-Day MA"
        ), row=1, col=1)

    # volume colored by up/down day
    if "Volume" in data.columns:
        vol = data["Volume"].astype(float)
        prev_close = data["Close"].shift(1)
        up = data["Close"] >= prev_close
        colors = ["#20c997" if x else "#ff4d4d" for x in up.fillna(False)]
        fig.add_trace(go.Bar(
            x=data.index,
            y=vol,
            marker_color=colors,
            marker_line_width=0.5,
            marker_line_color="#111111",
            opacity=0.9,
            name="Volume",
            showlegend=False,
            hovertemplate="%{x|%b %d, %Y}<br><b>Volume:</b> %{y:,}<extra></extra>"
        ), row=2, col=1)

    # layout polish
    fig.update_layout(
        template="plotly_dark",
        height=620,
        margin=dict(l=60, r=20, t=40, b=60),
        bargap=0.12,
        bargroupgap=0.02,
        xaxis=dict(rangeselector=dict(buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=3, label="3m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(step="all")
        ])), rangeslider=dict(visible=False), type="date"),
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    fig.update_yaxes(row=1, tickprefix="$", separatethousands=True)
    fig.update_yaxes(row=2, tickformat=",.0f", separatethousands=True)
    fig.update_xaxes(showgrid=False)

    return fig

def multi_plot(ticker_list, start, end):
    fig = go.Figure()
    for tick in ticker_list:
        data = yf.download(tick, start=start, end=end)
        if data is None:
            continue
        # Normalize Series -> DataFrame for single-row downloads
        if isinstance(data, pd.Series):
            try:
                data = data.to_frame().T
            except Exception:
                data = pd.DataFrame([data])
        if not data.empty:
            # guard: ensure 'Close' in columns
            if "Close" in data.columns:
                try:
                    data.index = pd.to_datetime(data.index)
                except Exception:
                    pass
                data = data.sort_index()
                y = data["Close"].astype(float)
                # normalize to 100 at the start to compare growth
                try:
                    base = float(y.iloc[0])
                    norm = (y / base) * 100
                except Exception:
                    norm = y
                mode_m = "lines+markers" if len(norm) < 10 else "lines"
                fig.add_trace(go.Scatter(x=data.index, y=norm, mode=mode_m, name=tick, hovertemplate="%{x|%b %d, %Y}<br><b>%{fullData.name}:</b> %{y:.2f}<extra></extra>"))
    fig.update_layout(title="Indexed Close Prices (Base = 100)", xaxis_title="Date", yaxis_title="Index (100 = start)", template="plotly_dark", height=420)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(separatethousands=True)
    return fig

# Load and process data
df = get_data(ticker, start_date, end_date)
df.to_csv("stock_data.csv")

if df.empty:
    st.warning("No data found for this ticker and date range.")
else:
    df = calculate_moving_average(df, ma_window)
    df = calculate_rsi(df, rsi_period)

    # Top metrics
    if len(df) >= 2:
        latest = df["Close"].iloc[-1]
        prev = df["Close"].iloc[-2]
        # Normalize possible Series/Array to scalars (yfinance can sometimes return Series)
        try:
            if isinstance(latest, (pd.Series, pd.DataFrame)):
                latest = latest.iloc[-1]
        except Exception:
            pass
        try:
            if isinstance(prev, (pd.Series, pd.DataFrame)):
                prev = prev.iloc[-1]
        except Exception:
            pass
        try:
            latest_val = float(latest)
        except Exception:
            latest_val = None
        try:
            prev_val = float(prev)
        except Exception:
            prev_val = None

        if prev_val in (None, 0):
            change = 0
            pct = 0
        else:
            change = latest_val - prev_val
            pct = (change / prev_val) * 100
    else:
        latest = df["Close"].iloc[-1]
        # ensure scalar
        try:
            if isinstance(latest, (pd.Series, pd.DataFrame)):
                latest = latest.iloc[-1]
        except Exception:
            pass
        change = 0
        pct = 0

    mcol1, mcol2, mcol3 = st.columns([2, 1, 1])
    mcol1.metric(label=f"{ticker} Last Close", value=f"${latest:,.2f}", delta=f"{pct:.2f}%")
    mcol2.metric(label="MA Window", value=f"{ma_window}-day")
    mcol3.metric(label="RSI Period", value=f"{rsi_period}")

    # Raw data in an expander to save space
    with st.expander("Raw Data (Last 5 rows)", expanded=False):
        st.dataframe(df.tail())

    # Combined price + volume chart (professional, shared x-axis)
    st.subheader("Price Chart with Moving Average")
    st.plotly_chart(plot_price_with_volume(df, ticker), width='stretch')

    # Also expose a dedicated volume chart (collapsible) so users can inspect volume-only view
    with st.expander("Daily Trading Volume (separate)", expanded=False):
        st.plotly_chart(plot_volume(df, ticker), width='stretch')

    # RSI
    st.subheader("RSI Indicator")
    st.plotly_chart(plot_rsi(df, ticker), width='stretch')

    # CSV download
    csv = df.to_csv().encode("utf-8")
    st.download_button(
        label="📅 Download Data as CSV",
        data=csv,
        file_name=f"{ticker}_data.csv",
        mime="text/csv"
    )

# Optional: Compare multiple stocks
tickers_input = st.sidebar.text_input("Compare Tickers (comma-separated)", value="AAPL,TSLA")
compare = st.sidebar.checkbox("Show Comparison Chart")

if compare:
    ticker_list = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
    st.subheader(":bar_chart: Compare Multiple Stocks")
    st.plotly_chart(multi_plot(ticker_list, start_date, end_date), width='stretch')
