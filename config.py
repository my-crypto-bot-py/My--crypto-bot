# ==========================
# SYMBOLS
# ==========================

SYMBOLS = [
    "BTCUSDT",
    "ETHUSDT",
    "SOLUSDT",
    "XRPUSDT"
]

# ==========================
# TIMEFRAMES
# ==========================

TIMEFRAMES = {
    "BIAS": "1d",          # Overall Market Bias
    "TREND": "4h",         # Main Trend
    "STRUCTURE": "1h",     # BOS / MSS / CHoCH
    "POI": "30m",          # Order Block / FVG
    "ENTRY": "15m",        # Liquidity + MSS
    "EXECUTION": "5m"      # Exact Entry
}

# ==========================
# RISK MANAGEMENT
# ==========================

RISK_PERCENT = 1

RISK_REWARD = {
    "TP1": 3,
    "TP2": 4
}

ATR_PERIOD = 14
ATR_MULTIPLIER = 1.5

ENTRY_BUFFER = 15

# ==========================
# SIGNAL FILTER
# ==========================

MIN_CONFIDENCE = 85

LOOKBACK = 20

# ==========================
# TRADING SESSIONS (UTC)
# ==========================

USE_LONDON = True
USE_NEWYORK = True

LONDON_SESSION = {
    "start": 7,
    "end": 16
}

NEWYORK_SESSION = {
    "start": 13,
    "end": 22
}

# ==========================
# BTC CORRELATION
# ==========================

USE_BTC_CONFIRMATION = True

CORRELATION_PERIOD = 50

# ==========================
# SMART MONEY FILTERS
# ==========================

USE_LIQUIDITY_SWEEP = True
USE_FVG = True
USE_ORDER_BLOCK = True
USE_CHOCH = True
USE_MSS = True
USE_BOS = True

# ==========================
# TELEGRAM
# ==========================

SEND_ONLY_HIGH_CONFIDENCE = True
