from datetime import datetime


# ==========================
# UTC HOUR
# ==========================

def get_utc_hour():

    return datetime.utcnow().hour


# ==========================
# ASIAN SESSION
# 00:00 - 08:00 UTC
# ==========================

def is_asian_session():

    hour = get_utc_hour()

    return 0 <= hour < 8


# ==========================
# LONDON SESSION
# 08:00 - 16:00 UTC
# ==========================

def is_london_session():

    hour = get_utc_hour()

    return 8 <= hour < 16


# ==========================
# NEW YORK SESSION
# 13:00 - 21:00 UTC
# ==========================

def is_newyork_session():

    hour = get_utc_hour()

    return 13 <= hour < 21


# ==========================
# LONDON KILL ZONE
# 07:00 - 10:00 UTC
# ==========================

def london_killzone():

    hour = get_utc_hour()

    return 7 <= hour < 10


# ==========================
# NEW YORK KILL ZONE
# 13:00 - 16:00 UTC
# ==========================

def newyork_killzone():

    hour = get_utc_hour()

    return 13 <= hour < 16
  # ==========================
# SESSION HIGH / LOW
# ==========================

def get_session_high_low(df):

    high = float(df["high"].max())
    low = float(df["low"].min())

    return {

        "high": high,

        "low": low

    }


# ==========================
# ASIAN RANGE
# ==========================

def get_asian_range(df):

    session = df.iloc[-96:] if len(df) >= 96 else df

    return get_session_high_low(session)


# ==========================
# LONDON RANGE
# ==========================

def get_london_range(df):

    session = df.iloc[-48:] if len(df) >= 48 else df

    return get_session_high_low(session)


# ==========================
# NEW YORK RANGE
# ==========================

def get_newyork_range(df):

    session = df.iloc[-48:] if len(df) >= 48 else df

    return get_session_high_low(session)


# ==========================
# SESSION LIQUIDITY
# ==========================

def get_session_liquidity(df):

    asian = get_asian_range(df)

    london = get_london_range(df)

    newyork = get_newyork_range(df)

    return {

        "asian": asian,

        "london": london,

        "newyork": newyork

    }
  # ==========================
# JUDAS SWING
# ==========================

def detect_judas_swing(df):

    if len(df) < 20:
        return None

    asian = get_asian_range(df)

    last = df.iloc[-1]

    # Buy-side Judas
    if (
        float(last["high"]) > asian["high"]
        and float(last["close"]) < asian["high"]
    ):

        return {
            "direction": "SELL",
            "type": "Judas Buy Sweep"
        }

    # Sell-side Judas
    if (
        float(last["low"]) < asian["low"]
        and float(last["close"]) > asian["low"]
    ):

        return {
            "direction": "BUY",
            "type": "Judas Sell Sweep"
        }

    return None


# ==========================
# SESSION SWEEP
# ==========================

def detect_session_sweep(df):

    if len(df) < 20:
        return None

    asian = get_asian_range(df)

    london = get_london_range(df)

    last = df.iloc[-1]

    # London takes Asian High
    if (
        float(last["high"]) > asian["high"]
        and london_killzone()
    ):

        return {
            "direction": "SELL",
            "type": "London High Sweep"
        }

    # London takes Asian Low
    if (
        float(last["low"]) < asian["low"]
        and london_killzone()
    ):

        return {
            "direction": "BUY",
            "type": "London Low Sweep"
        }

    return None


# ==========================
# SESSION SUMMARY
# ==========================

def analyze_sessions(df):

    return {

        "asian": is_asian_session(),

        "london": is_london_session(),

        "newyork": is_newyork_session(),

        "london_kz": london_killzone(),

        "newyork_kz": newyork_killzone(),

        "judas": detect_judas_swing(df),

        "session_sweep": detect_session_sweep(df)

    }
