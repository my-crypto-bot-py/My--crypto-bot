import telebot
import time


# ==========================
# TELEGRAM BOT ENGINE V5
# ==========================


# ==========================
# SETTINGS
# ==========================

TELEGRAM_TOKEN = ""

CHAT_ID = ""



# ==========================
# BOT INIT
# ==========================

bot = telebot.TeleBot(

    TELEGRAM_TOKEN

)



# ==========================
# BOT STATE
# ==========================

bot_state = {

    "messages": 0,

    "last_signal": None,

    "status": "ACTIVE"

}



# ==========================
# CREATE MESSAGE
# ==========================

def create_message(

    signal

):

    if signal is None:

        return "⚠️ No Signal"


    return f"""

🚀 TRADING SIGNAL

Symbol: {signal.get('symbol')}

Direction: {signal.get('direction')}

Entry: {signal.get('entry')}

SL: {signal.get('sl')}

TP: {signal.get('tp')}

Confidence: {signal.get('confidence')}%

"""
    # ==========================
# SEND MESSAGE
# ==========================

def send_message(

    message

):

    try:

        if not CHAT_ID:

            return False


        bot.send_message(

            CHAT_ID,

            message

        )


        bot_state["messages"] += 1


        return True


    except Exception as e:

        print(

            "Telegram Error:",

            e

        )

        return False



# ==========================
# SEND SIGNAL
# ==========================

def send_signal(

    signal

):

    message = create_message(

        signal

    )


    success = send_message(

        message

    )


    if success:

        bot_state["last_signal"] = signal


    return success



# ==========================
# ERROR MESSAGE
# ==========================

def send_error(

    error

):

    message = f"""

⚠️ BOT ERROR

{error}

"""


    return send_message(

        message

    )
    # ==========================
# SIGNAL FORMATTER
# ==========================

def format_signal(

    signal

):

    if signal is None:

        return "⚠️ No valid signal"



    direction = signal.get(

        "direction",

        "N/A"

    )


    emoji = (

        "🟢"

        if direction == "BUY"

        else

        "🔴"

        if direction == "SELL"

        else

        "⚪"

    )


    return f"""

{emoji} SMART MONEY SIGNAL

📌 Symbol: {signal.get('symbol')}

📈 Direction: {direction}

🎯 Entry: {signal.get('entry')}

🛑 Stop Loss: {signal.get('sl')}

✅ Take Profit: {signal.get('tp')}

🔥 Confidence: {signal.get('confidence')}%

"""



# ==========================
# RISK REPORT FORMAT
# ==========================

def format_risk_report(

    risk

):

    if risk is None:

        return "⚠️ Risk data unavailable"



    return f"""

🛡 RISK REPORT

RR: {risk.get('rr')}

Position Size: {risk.get('position_size')}

Margin: {risk.get('margin')}

Risk Score: {risk.get('risk_score')}

"""
    # ==========================
# FINAL ALERT BUILDER
# ==========================

def build_alert(

    signal,

    risk=None

):

    message = ""


    message += format_signal(

        signal

    )


    if risk:

        message += format_risk_report(

            risk

        )


    return message



# ==========================
# SEND FINAL ALERT
# ==========================

def send_trade_alert(

    signal,

    risk=None

):

    alert = build_alert(

        signal,

        risk

    )


    return send_message(

        alert

    )



# ==========================
# NO TRADE ALERT
# ==========================

def send_no_trade_alert(

    reason="Low Confidence"

):

    message = f"""

⚪ NO TRADE

Reason: {reason}

"""


    return send_message(

        message

    )
    # ==========================
# BOT COMMANDS
# ==========================

@bot.message_handler(commands=["start"])
def start_command(

    message

):

    text = """

🤖 Smart Money Bot V5

Status: ACTIVE

Commands:

/status
/signal
/help

"""


    bot.send_message(

        message.chat.id,

        text

    )



# ==========================
# STATUS COMMAND
# ==========================

@bot.message_handler(commands=["status"])
def status_command(

    message

):

    text = f"""

📊 BOT STATUS

State: {bot_state["status"]}

Messages Sent: {bot_state["messages"]}

Last Signal:

{bot_state["last_signal"]}

"""


    bot.send_message(

        message.chat.id,

        text

    )



# ==========================
# HELP COMMAND
# ==========================

@bot.message_handler(commands=["help"])
def help_command(

    message

):

    text = """

Available Commands:

/start - Start bot

/status - Bot status

/signal - Latest signal

"""


    bot.send_message(

        message.chat.id,

        text

    )
    # ==========================
# SIGNAL COMMAND
# ==========================

@bot.message_handler(commands=["signal"])
def signal_command(

    message

):

    last = bot_state["last_signal"]


    if last is None:

        text = """

⚪ No Signal Available

"""

    else:

        text = format_signal(

            last

        )


    bot.send_message(

        message.chat.id,

        text

    )



# ==========================
# CONNECTION TEST
# ==========================

def telegram_test():

    try:

        bot.get_me()


        return {

            "connected":

            True,

            "username":

            bot.get_me().username

        }


    except Exception as e:

        return {

            "connected":

            False,

            "error":

            str(e)

        }



# ==========================
# BOT RUNNER
# ==========================

def run_bot():

    print(

        "Telegram Bot V5 Started..."

    )


    bot.infinity_polling()
    # ==========================
# SCANNER CONNECTION
# ==========================

def get_scanner_signal():

    try:

        from scanner import (

            run_scanner

        )


        result = run_scanner()


        return result.get(

            "signal"

        )


    except Exception as e:

        print(

            "Scanner Error:",

            e

        )

        return None



# ==========================
# AUTO SIGNAL CHECK
# ==========================

def auto_signal_check():

    signal = get_scanner_signal()


    if signal is None:

        return False


    send_trade_alert(

        signal

    )


    return True



# ==========================
# BOT LOOP
# ==========================

def bot_signal_loop():

    while True:

        try:

            auto_signal_check()


        except Exception as e:

            send_error(

                str(e)

            )


        time.sleep(

            60

        )
        # ==========================
# ADVANCED SIGNAL MESSAGE
# ==========================

def advanced_signal_message(

    signal,

    confidence=None,

    risk=None

):

    if signal is None:

        return "⚪ No Signal"



    message = f"""

🚀 SMART MONEY ALERT V5

━━━━━━━━━━━━━━

📌 Symbol:
{signal.get('symbol')}

📈 Direction:
{signal.get('direction')}

🎯 Entry:
{signal.get('entry')}

🛑 Stop Loss:
{signal.get('sl')}

✅ Take Profit:
{signal.get('tp')}

🔥 Confidence:
{confidence if confidence else signal.get('confidence')}%

"""



    if risk:

        message += f"""

━━━━━━━━━━━━━━

🛡 Risk

RR:
{risk.get('rr')}

Position:
{risk.get('position_size')}

Risk Score:
{risk.get('risk_score')}

"""


    return message



# ==========================
# SEND ADVANCED ALERT
# ==========================

def send_advanced_alert(

    signal,

    confidence=None,

    risk=None

):

    message = advanced_signal_message(

        signal,

        confidence,

        risk

    )


    return send_message(

        message

    )
    # ==========================
# BOT DEBUG PANEL
# ==========================

def debug_bot():

    print("\n========== TELEGRAM BOT V5 ==========")

    print(

        "Status:",

        bot_state["status"]

    )

    print(

        "Messages:",

        bot_state["messages"]

    )

    print(

        "Last Signal:",

        bot_state["last_signal"]

    )

    print(

        "=====================================\n"

    )


    return bot_state



# ==========================
# BOT REPORT
# ==========================

def bot_report():

    return {

        "status":

        bot_state["status"],

        "messages":

        bot_state["messages"],

        "last_signal":

        bot_state["last_signal"]

    }



# ==========================
# RESET BOT
# ==========================

def reset_bot():

    bot_state["messages"] = 0

    bot_state["last_signal"] = None

    bot_state["status"] = "ACTIVE"


    return True
    # ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def telegram_bot_engine_v5():

    return {

        "status":

        bot_state["status"],

        "messages":

        bot_state["messages"],

        "last_signal":

        bot_state["last_signal"]

    }



# ==========================
# FULL BOT START
# ==========================

def start_telegram_service():

    try:

        print(

            "Telegram Service V5 Started"

        )


        run_bot()


    except Exception as e:

        send_error(

            str(e)

        )



# ==========================
# EXPORTS
# ==========================

__all__ = [

    "send_message",

    "send_signal",

    "send_trade_alert",

    "send_advanced_alert",

    "format_signal",

    "format_risk_report",

    "telegram_test",

    "run_bot",

    "bot_report",

    "debug_bot",

    "reset_bot",

    "telegram_bot_engine_v5",

    "start_telegram_service"

]
