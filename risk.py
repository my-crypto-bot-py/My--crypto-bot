# ==========================
# RISK MANAGEMENT
# ==========================

def calculate_rr(entry, sl, tp):

    risk = abs(entry - sl)
    reward = abs(tp - entry)

    if risk == 0:
        return 0

    return round(reward / risk, 2)


# ==========================
# POSITION SIZE
# ==========================

def calculate_position_size(

    balance,
    risk_percent,
    entry,
    sl

):

    risk_amount = balance * (risk_percent / 100)

    stop_distance = abs(entry - sl)

    if stop_distance == 0:
        return 0

    size = risk_amount / stop_distance

    return round(size, 4)


# ==========================
# VALIDATE TRADE
# ==========================

def validate_trade(

    entry,
    sl,
    tp,
    min_rr=3

):

    rr = calculate_rr(
        entry,
        sl,
        tp
    )

    if rr < min_rr:

        return {

            "valid": False,

            "rr": rr

        }

    return {

        "valid": True,

        "rr": rr

    }
   # ==========================
# DAILY LOSS LIMIT
# ==========================

daily_loss = 0
max_daily_loss = 3      # %

trade_count = 0
max_trades = 5

consecutive_losses = 0
max_consecutive_losses = 3


# ==========================
# CAN TAKE TRADE
# ==========================

def can_take_trade():

    global daily_loss
    global trade_count
    global consecutive_losses

    if daily_loss >= max_daily_loss:

        return False, "Daily Loss Limit Reached"

    if trade_count >= max_trades:

        return False, "Maximum Trades Reached"

    if consecutive_losses >= max_consecutive_losses:

        return False, "Too Many Consecutive Losses"

    return True, "OK"


# ==========================
# UPDATE RESULT
# ==========================

def update_trade_result(result, loss_percent=1):

    global daily_loss
    global trade_count
    global consecutive_losses

    trade_count += 1

    if result == "LOSS":

        consecutive_losses += 1
        daily_loss += loss_percent

    elif result == "WIN":

        consecutive_losses = 0


# ==========================
# RESET NEW DAY
# ==========================

def reset_daily_stats():

    global daily_loss
    global trade_count
    global consecutive_losses

    daily_loss = 0
    trade_count = 0
    consecutive_losses = 0
