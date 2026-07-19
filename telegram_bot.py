# ==========================
# TELEGRAM BOT V2
# ==========================

import os
import telebot



# ==========================
# ENV
# ==========================

TOKEN = os.getenv(
    "TELEGRAM_TOKEN"
)

CHAT_ID = os.getenv(
    "CHAT_ID"
)



if not TOKEN:

    raise Exception(
        "TELEGRAM_TOKEN missing"
    )



if not CHAT_ID:

    raise Exception(
        "CHAT_ID missing"
    )




bot = telebot.TeleBot(
    TOKEN
)




# ==========================
# SEND SIGNAL
# ==========================

def send_signal(data):


    reasons = data.get(
        "reasons",
        []
    )



    if isinstance(
        reasons,
        list
    ):

        reasons = "\n✔ ".join(
            reasons
        )


    else:

        reasons = str(
            reasons
        )




    message = f"""

🚀 ICT SMART MONEY SIGNAL


🪙 Symbol:
{data.get("symbol","N/A")}


📈 Signal:
{data.get("signal","N/A")}


📊 Trend:
{data.get("trend","N/A")}


🎯 Entry:
{data.get("entry","N/A")}


🛑 SL:
{data.get("sl","N/A")}


✅ TP1:
{data.get("tp1","N/A")}


✅ TP2:
{data.get("tp2","N/A")}


📐 RR:
{data.get("rr","N/A")}


🔥 Score:
{data.get("score","N/A")}%


📍 Zone:
{data.get("zone","N/A")}


📋 Confirmation:

✔ {reasons}


"""


    try:


        print(
            "Sending Telegram Signal..."
        )


        bot.send_message(

            CHAT_ID,

            message

        )



        print(

            "Telegram Sent Successfully"

        )



        return True



    except Exception as e:


        print(

            "Telegram Error:",

            e

        )


        return False
