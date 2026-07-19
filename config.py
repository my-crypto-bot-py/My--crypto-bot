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

HTF = "1d"
TREND_TF = "4h"
POI_TF = "1h"
ENTRY_TF = "5m"

# ==========================
# MARKET
# ==========================

LIMIT = 300

# ==========================
# SWINGS
# ==========================

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

# ==========================
# RISK
# ==========================

MIN_RR = 3.0
RISK_PERCENT = 1

# ==========================
# BTC FILTER
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
# DUPLICATE FILTER
# ==========================

COOLDOWN_MINUTES = 60
MAX_TRADES_PER_DAY = 5
MAX_DAILY_LOSS = 3
MAX_CONSECUTIVE_LOSSES = 3
