# ==========================
# ICT OTE ENGINE
# ==========================

def fibonacci_levels(high, low):

    diff = high - low

    return {

        "0.50": high - (diff * 0.50),

        "0.618": high - (diff * 0.618),

        "0.705": high - (diff * 0.705),

        "0.79": high - (diff * 0.79)

    }


# ==========================
# BUY OTE
# ==========================

def buy_ote(high, low):

    fib = fibonacci_levels(high, low)

    return {

        "entry": fib["0.705"],

        "discount": fib["0.618"],

        "deep_discount": fib["0.79"]

    }


# ==========================
# SELL OTE
# ==========================

def sell_ote(high, low):

    diff = high - low

    return {

        "entry": low + (diff * 0.705),

        "premium": low + (diff * 0.618),

        "deep_premium": low + (diff * 0.79)

    }
  # ==========================
# PRICE INSIDE OTE
# ==========================

def is_price_in_ote(price, high, low, direction):

    if direction == "BUY":

        ote = buy_ote(high, low)

        return (
            ote["deep_discount"]
            <= price
            <= ote["discount"]
        )

    elif direction == "SELL":

        ote = sell_ote(high, low)

        return (
            ote["premium"]
            <= price
            <= ote["deep_premium"]
        )

    return False


# ==========================
# BEST OTE ENTRY
# ==========================

def get_best_ote(high, low, direction):

    if direction == "BUY":

        return buy_ote(high, low)

    elif direction == "SELL":

        return sell_ote(high, low)

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

    ote = get_best_ote(
        high,
        low,
        direction
    )

    return {

        "valid": valid,

        "entry": ote["entry"],

        "zone": ote

    }
  # ==========================
# OTE + STRUCTURE CONFIRMATION
# ==========================

def ote_structure_confirmation(
    ote_valid,
    bos=None,
    mss=None,
    choch=None
):

    if not ote_valid:
        return False


    if (
        bos
        or mss
        or choch
    ):

        return True


    return False



# ==========================
# OTE + FVG CONFIRMATION
# ==========================

def ote_fvg_confirmation(
    ote_valid,
    fvg=None,
    direction=None
):

    if not ote_valid:
        return False


    if fvg:

        if fvg.get("direction") == direction:

            return True


    return False



# ==========================
# OTE + ORDER BLOCK
# ==========================

def ote_orderblock_confirmation(
    ote_valid,
    order_block=None,
    direction=None
):

    if not ote_valid:
        return False


    if order_block:

        if order_block.get("direction") == direction:

            return True


    return False



# ==========================
# FINAL OTE ENTRY ENGINE
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

            "valid": False,

            "reason": "Price not in OTE"

        }


    structure = ote_structure_confirmation(

        True,

        bos,

        mss,

        choch

    )


    fvg_confirm = ote_fvg_confirmation(

        True,

        fvg,

        direction

    )


    ob_confirm = ote_orderblock_confirmation(

        True,

        order_block,

        direction

    )


    confirmations = sum([

        structure,

        fvg_confirm,

        ob_confirm

    ])


    if confirmations >= 2:

        return {

            "valid": True,

            "entry": ote["entry"],

            "confirmations": confirmations

        }


    return {

        "valid": False,

        "reason": "Low Confirmation"

    }
