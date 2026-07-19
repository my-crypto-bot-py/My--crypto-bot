# ==========================
# SYMBOLS
# ==========================

SYMBOLS = [
    "BTC-USDT-SWAP",
    "ETH-USDT-SWAP",
    "SOL-USDT-SWAP",
    "XRP-USDT-SWAP"
]


# ==========================
# TIMEFRAMES
# ==========================

HTF = "1d"          # Daily Bias
TREND_TF = "4h"      # Main Trend
POI_TF = "1h"        # Order Block / FVG
ENTRY_TF = "5m"      # Execution


# Main execution timeframe
TIMEFRAME = ENTRY_TF


# ==========================
# MARKET DATA
# ==========================

LIMIT = 300


# ==========================
# ICT SETTINGS
# ==========================

LOOKBACK = 50

LIQUIDITY_LOOKBACK = 20

SWING_LEFT = 5
SWING_RIGHT = 5


# ==========================
# ATR
# ==========================

ATR_PERIOD = 14

ATR_MULTIPLIER = 1.5


# ==========================
# EMA
# ==========================

EMA_FAST = 20

EMA_MID = 50

EMA_SLOW = 200


# ==========================
# CONFIDENCE
# ==========================

MIN_SCORE = 70

MIN_EXECUTION_SCORE = 70


# ==========================
# RISK MANAGEMENT
# ==========================

MIN_RR = 3.0

RISK_PERCENT = 1


# ==========================
# ACCOUNT
# ==========================

ACCOUNT_BALANCE = 1000


# ==========================
# BTC CONFIRMATION
# ==========================

BTC_CONFIRMATION = True


# ==========================
# VOLUME
# ==========================

VOLUME_CONFIRMATION = True


# ==========================
# SESSIONS
# ==========================

LONDON_SESSION = True

NEWYORK_SESSION = True


# ==========================
# FILTERS
# ==========================

COOLDOWN_MINUTES = 60

MAX_TRADES_PER_DAY = 5

MAX_DAILY_LOSS = 3

MAX_CONSECUTIVE_LOSSES = 3


# ==========================
# TELEGRAM
# ==========================

ENABLE_TELEGRAM = True
