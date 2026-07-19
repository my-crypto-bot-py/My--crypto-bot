# ==========================
# ICT SMT DIVERGENCE ENGINE V2
# ==========================


# ==========================
# GET SWING POINTS
# ==========================

def get_recent_high_low(
    df,
    lookback=50
):

    data = df.tail(
        lookback
    )


    return {

        "high":
        float(data["high"].max()),


        "low":
        float(data["low"].min())

    }



# ==========================
# COMPARE MARKETS
# ==========================

def compare_markets(
    main_df,
    compare_df
):

    main = get_recent_high_low(
        main_df
    )


    comp = get_recent_high_low(
        compare_df
    )


    return {

        "main_high":
        main["high"],


        "main_low":
        main["low"],


        "compare_high":
        comp["high"],


        "compare_low":
        comp["low"]

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


    # Main takes low liquidity
    # Compare fails to take low


    if (

        data["main_low"]
        <
        data["compare_low"]

        and

        data["compare_low"]
        >
        data["main_low"]

    ):


        return {

            "direction":
            "BUY",

            "type":
            "Bullish SMT",

            "reason":
            "Main market lower low, second market no confirmation",

            "confirm":
            True

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


    # Main takes high liquidity
    # Compare fails to take high


    if (

        data["main_high"]
        >
        data["compare_high"]

        and

        data["compare_high"]
        <
        data["main_high"]

    ):


        return {

            "direction":
            "SELL",

            "type":
            "Bearish SMT",

            "reason":
            "Main market higher high, second market no confirmation",

            "confirm":
            True

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



    return {

        "confirm":
        False,

        "direction":
        None,

        "reason":
        "No SMT Divergence"

    }




# ==========================
# MULTI MARKET SMT
# ==========================

def get_smt_confirmation(

    btc_df,

    eth_df=None,

    sol_df=None

):


    results = []



    if eth_df is not None:


        eth_smt = detect_smt(

            btc_df,

            eth_df

        )


        if eth_smt.get("confirm"):

            results.append(
                eth_smt
            )



    if sol_df is not None:


        sol_smt = detect_smt(

            btc_df,

            sol_df

        )


        if sol_smt.get("confirm"):

            results.append(
                sol_smt
            )



    if len(results) == 0:


        return {

            "confirm":
            False,

            "direction":
            None,

            "reason":
            "No SMT Confirmation"

        }



    # Same direction check

    buy = 0
    sell = 0



    for r in results:


        if r["direction"] == "BUY":

            buy += 1


        elif r["direction"] == "SELL":

            sell += 1



    if buy > sell:


        return {

            "confirm":
            True,

            "direction":
            "BUY",

            "type":
            "Multi Market Bullish SMT",

            "strength":
            buy

        }



    elif sell > buy:


        return {

            "confirm":
            True,

            "direction":
            "SELL",

            "type":
            "Multi Market Bearish SMT",

            "strength":
            sell

        }



    return {

        "confirm":
        False,

        "direction":
        None,

        "reason":
        "SMT Conflict"

    }
