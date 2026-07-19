# ==========================
# ICT OTE ENGINE V2
# ==========================


def fibonacci_levels(high, low):

    if high <= low:
        return None

    diff = high - low

    return {

        "50": high - (diff * 0.50),

        "618": high - (diff * 0.618),

        "705": high - (diff * 0.705),

        "79": high - (diff * 0.79)

    }



# ==========================
# BUY OTE
# ==========================

def buy_ote(high, low):

    fib = fibonacci_levels(
        high,
        low
    )

    if fib is None:
        return None


    return {

        "direction":"BUY",

        "entry":fib["705"],

        "ote_low":fib["79"],

        "ote_high":fib["618"]

    }



# ==========================
# SELL OTE
# ==========================

def sell_ote(high, low):

    if high <= low:
        return None


    diff = high - low


    return {

        "direction":"SELL",

        "entry":
        low + (diff * 0.705),


        "ote_low":
        low + (diff * 0.618),


        "ote_high":
        low + (diff * 0.79)

    }



# ==========================
# PRICE IN OTE ZONE
# ==========================

def is_price_in_ote(
    price,
    high,
    low,
    direction
):


    if direction == "BUY":

        ote = buy_ote(
            high,
            low
        )


    elif direction == "SELL":

        ote = sell_ote(
            high,
            low
        )


    else:

        return False



    if ote is None:
        return False



    return (

        ote["ote_low"]
        <= price
        <= ote["ote_high"]

    )
    # ==========================
# GET OTE ZONE
# ==========================

def get_best_ote(
    high,
    low,
    direction
):

    if direction == "BUY":

        return buy_ote(
            high,
            low
        )


    elif direction == "SELL":

        return sell_ote(
            high,
            low
        )


    return None



# ==========================
# OTE CONFIRMATION
# ==========================

def confirm_ote(

    price,

    high,

    low,

    direction

):

    valid = is_price_in_ote(

        price,

        high,

        low,

        direction

    )


    zone = get_best_ote(

        high,

        low,

        direction

    )


    if zone is None:

        return {

            "valid":False,

            "reason":"Invalid OTE Zone"

        }



    return {

        "valid":valid,

        "direction":direction,

        "entry":zone["entry"],

        "zone":zone

    }



# ==========================
# STRUCTURE CONFIRMATION
# ==========================

def confirm_structure(

    bos=None,

    mss=None,

    choch=None,

    direction=None

):

    confirmations = 0


    for item in [
        bos,
        mss,
        choch
    ]:

        if item:

            if item.get(
                "direction"
            ) == direction:

                confirmations += 1



    return confirmations > 0




# ==========================
# FVG CONFIRMATION
# ==========================

def confirm_fvg(

    fvg=None,

    direction=None

):

    if not fvg:

        return False


    return (

        fvg.get("direction")
        ==
        direction

    )




# ==========================
# ORDER BLOCK CONFIRMATION
# ==========================

def confirm_order_block(

    order_block=None,

    direction=None

):

    if not order_block:

        return False


    return (

        order_block.get("direction")
        ==
        direction

    )



# ==========================
# INSTITUTIONAL OTE ENTRY
# ==========================

def institutional_ote_entry(

    price,

    high,

    low,

    direction,

    bos=None,

    mss=None,

    choch=None,

    fvg=None,

    order_block=None

):


    ote = confirm_ote(

        price,

        high,

        low,

        direction

    )


    if not ote["valid"]:

        return {

            "valid":False,

            "reason":
            "Price Outside OTE"

        }



    structure = confirm_structure(

        bos,

        mss,

        choch,

        direction

    )


    fvg_confirm = confirm_fvg(

        fvg,

        direction

    )


    ob_confirm = confirm_order_block(

        order_block,

        direction

    )


    score = 0


    if structure:

        score += 40


    if fvg_confirm:

        score += 30


    if ob_confirm:

        score += 30



    if score >= 70:

        return {

            "valid":True,

            "direction":direction,

            "entry":ote["entry"],

            "score":score,

            "confirmations":{

                "structure":structure,

                "fvg":fvg_confirm,

                "order_block":ob_confirm

            }

        }



    return {

        "valid":False,

        "score":score,

        "reason":
        "Low OTE Confirmation"

    }
