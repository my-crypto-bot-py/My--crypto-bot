# ==========================
# SMT DIVERGENCE ENGINE
# ==========================


# ==========================
# GET RECENT HIGH / LOW
# ==========================

def get_recent_high_low(df, lookback=50):

    data = df.tail(lookback)

    high = float(data["high"].max())

    low = float(data["low"].min())

    return {

        "high": high,

        "low": low

    }



# ==========================
# MARKET STRUCTURE POINT
# ==========================

def get_market_points(df):

    recent = get_recent_high_low(df)

    return {

        "high": recent["high"],

        "low": recent["low"]

    }



# ==========================
# COMPARE TWO MARKETS
# ==========================

def compare_markets(
    main_df,
    compare_df
):

    main = get_market_points(main_df)

    comp = get_market_points(compare_df)


    return {

        "main_high": main["high"],

        "main_low": main["low"],

        "compare_high": comp["high"],

        "compare_low": comp["low"]

    }
  # ==========================
# BULLISH SMT
# ==========================

def detect_bullish_smt(
    main_df,
    compare_df
):

    data = compare_markets(
        main_df,
        compare_df
    )


    # Main market makes lower low
    # Compare market fails to make lower low

    if (
        data["main_low"] < data["compare_low"]
        and
        data["compare_low"] > data["main_low"]
    ):

        return {

            "direction": "BUY",

            "type": "Bullish SMT",

            "reason":
            "Lower Low divergence"

        }


    return None



# ==========================
# BEARISH SMT
# ==========================

def detect_bearish_smt(
    main_df,
    compare_df
):

    data = compare_markets(
        main_df,
        compare_df
    )


    # Main market makes higher high
    # Compare market fails to make higher high

    if (
        data["main_high"] > data["compare_high"]
        and
        data["compare_high"] < data["main_high"]
    ):

        return {

            "direction": "SELL",

            "type": "Bearish SMT",

            "reason":
            "Higher High divergence"

        }


    return None



# ==========================
# FINAL SMT CHECK
# ==========================

def detect_smt(
    main_df,
    compare_df
):

    bullish = detect_bullish_smt(
        main_df,
        compare_df
    )


    if bullish:

        return bullish


    bearish = detect_bearish_smt(
        main_df,
        compare_df
    )


    if bearish:

        return bearish


    return None
  # ==========================
# BULLISH SMT
# ==========================

def detect_bullish_smt(
    main_df,
    compare_df
):

    data = compare_markets(
        main_df,
        compare_df
    )


    # Main market makes lower low
    # Compare market fails to make lower low

    if (
        data["main_low"] < data["compare_low"]
        and
        data["compare_low"] > data["main_low"]
    ):

        return {

            "direction": "BUY",

            "type": "Bullish SMT",

            "reason":
            "Lower Low divergence"

        }


    return None



# ==========================
# BEARISH SMT
# ==========================

def detect_bearish_smt(
    main_df,
    compare_df
):

    data = compare_markets(
        main_df,
        compare_df
    )


    # Main market makes higher high
    # Compare market fails to make higher high

    if (
        data["main_high"] > data["compare_high"]
        and
        data["compare_high"] < data["main_high"]
    ):

        return {

            "direction": "SELL",

            "type": "Bearish SMT",

            "reason":
            "Higher High divergence"

        }


    return None



# ==========================
# FINAL SMT CHECK
# ==========================

def detect_smt(
    main_df,
    compare_df
):

    bullish = detect_bullish_smt(
        main_df,
        compare_df
    )


    if bullish:

        return bullish


    bearish = detect_bearish_smt(
        main_df,
        compare_df
    )


    if bearish:

        return bearish


    return None
