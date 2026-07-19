import pandas as pd


# ==========================
# EXTERNAL RANGE
# ==========================

def get_external_range(df, lookback=200):

    if len(df) < lookback:
        lookback = len(df)

    data = df.tail(lookback)

    high = float(data["high"].max())
    low = float(data["low"].min())

    return {
        "high": high,
        "low": low,
        "range": high - low
    }


# ==========================
# INTERNAL RANGE
# ==========================

def get_internal_range(df, lookback=40):

    if len(df) < lookback:
        lookback = len(df)

    data = df.tail(lookback)

    high = float(data["high"].max())
    low = float(data["low"].min())

    return {
        "high": high,
        "low": low,
        "range": high - low
    }


# ==========================
# SWING HIGH
# ==========================

def get_last_swing_high(df, left=3, right=3):

    for i in range(
        len(df)-right-1,
        left,
        -1
    ):

        high = float(df["high"].iloc[i])

        if (
            high >
            df["high"].iloc[i-left:i].max()
            and
            high >
            df["high"].iloc[i+1:i+right+1].max()
        ):

            return {
                "index": i,
                "price": high
            }

    return None


# ==========================
# SWING LOW
# ==========================

def get_last_swing_low(df, left=3, right=3):

    for i in range(
        len(df)-right-1,
        left,
        -1
    ):

        low = float(df["low"].iloc[i])

        if (
            low <
            df["low"].iloc[i-left:i].min()
            and
            low <
            df["low"].iloc[i+1:i+right+1].min()
        ):

            return {
                "index": i,
                "price": low
            }

    return None
    # ==========================
# EQUILIBRIUM
# ==========================

def get_equilibrium(external_range):

    high = external_range["high"]
    low = external_range["low"]

    return round(
        (high + low) / 2,
        4
    )


# ==========================
# PREMIUM / DISCOUNT
# ==========================

def get_pd_zone(df, external_range):

    price = float(
        df["close"].iloc[-1]
    )

    high = external_range["high"]
    low = external_range["low"]

    equilibrium = (
        high + low
    ) / 2

    if price > equilibrium:

        zone = "Premium"

    elif price < equilibrium:

        zone = "Discount"

    else:

        zone = "Equilibrium"

    return {

        "price": round(price,4),

        "zone": zone,

        "equilibrium": round(
            equilibrium,
            4
        ),

        "high": round(high,4),

        "low": round(low,4)

    }


# ==========================
# DEALING RANGE
# ==========================

def get_dealing_range(df):

    ext = get_external_range(df)

    pd = get_pd_zone(
        df,
        ext
    )

    return {

        "external_high": ext["high"],

        "external_low": ext["low"],

        "equilibrium": pd["equilibrium"],

        "zone": pd["zone"]

    }


# ==========================
# PRICE POSITION
# ==========================

def get_price_position(df, external_range):

    high = external_range["high"]
    low = external_range["low"]

    price = float(
        df["close"].iloc[-1]
    )

    if high == low:
        return 50

    position = (
        (price - low)
        /
        (high - low)
    ) * 100

    return round(position,2)
   # ==========================
# EQUILIBRIUM
# ==========================

def get_equilibrium(high, low):

    return (high + low) / 2


# ==========================
# PREMIUM / DISCOUNT
# ==========================

def get_pd_zone(price, high, low):

    eq = get_equilibrium(high, low)

    if price > eq:

        zone = "Premium"

    elif price < eq:

        zone = "Discount"

    else:

        zone = "Equilibrium"

    return {

        "zone": zone,

        "equilibrium": eq,

        "price": price

    }


# ==========================
# DEALING RANGE
# ==========================

def get_dealing_range(df):

    ext = get_external_range(df)

    eq = get_equilibrium(

        ext["high"],

        ext["low"]

    )

    return {

        "high": ext["high"],

        "low": ext["low"],

        "equilibrium": eq

    }


# ==========================
# CURRENT PRICE POSITION
# ==========================

def current_pd_position(df):

    ext = get_external_range(df)

    price = float(df["close"].iloc[-1])

    return get_pd_zone(

        price,

        ext["high"],

        ext["low"]

    )
