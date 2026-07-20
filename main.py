import time


# ==========================
# IMPORT MODULES
# ==========================

from utils import *

from trend import *

from sessions import *

from signal import *

from filters import *

from scanner import *



# ==========================
# BOT STATE V5
# ==========================

BOT_STATE = {

    "running": False,

    "signals": 0,

    "errors": 0

}



# ==========================
# RESET BOT
# ==========================

def reset_bot():

    BOT_STATE["running"] = False

    BOT_STATE["signals"] = 0

    BOT_STATE["errors"] = 0


    reset_utils()

    reset_trend()

    reset_session()

    reset_signal()


    return True



# ==========================
# START BOT
# ==========================

def start_bot():

    BOT_STATE["running"] = True


    trade_log(

        "BOT V5 Started"

    )


    return True 
# ==========================
# MARKET DATA HANDLER
# ==========================

def get_market_data():

    try:

        from market import get_market_data as market_data


        data = market_data()


        return data


    except Exception as e:

        handle_error(

            e

        )

        return None



# ==========================
# DATA VALIDATION
# ==========================

def validate_market_data(

    data

):

    if data is None:

        return False


    return True



# ==========================
# MARKET CHECK
# ==========================

def market_check():

    data = get_market_data()


    if validate_market_data(

        data

    ):

        return True


    return False
# ==========================
# TREND CHECK
# ==========================

def check_market_trend(

    df

):

    try:

        result = trend_engine_v5(

            df

        )


        return result


    except Exception as e:

        handle_error(

            e

        )

        return None



# ==========================
# SESSION CHECK
# ==========================

def check_market_session():

    try:

        return sessions_engine_v5()


    except Exception as e:

        handle_error(

            e

        )

        return None



# ==========================
# MARKET BIAS PREPARATION
# ==========================

def prepare_market_bias(

    df

):

    trend = check_market_trend(

        df

    )


    session = check_market_session()


    return {

        "trend":

        trend,

        "session":

        session

    } 
# ==========================
# SCANNER CONNECTION
# ==========================
def run_scanner(

    market_data

):

    try:

        from scanner import run_market_scan


        result = run_market_scan()


        return result


    except Exception as e:

        handle_error(

            e

        )

        return None



# ==========================
# FILTER PIPELINE
# ==========================

def run_filters(

    setup

):

    try:

        result = final_trade_filter(

            setup

        )


        return result


    except Exception as e:

        handle_error(

            e

        )

        return False



# ==========================
# SIGNAL PIPELINE
# ==========================

def generate_signal(

    setup

):

    try:

        result = signal_engine_v5(

            setup

        )


        return result


    except Exception as e:

        handle_error(

            e

        )

        return None 
# ==========================
# PROCESS SIGNAL
# ==========================

def process_signal(

    setup

):

    try:

        approved = run_filters(

            setup

        )


        if not approved:

            return no_trade_signal(

                "Filter Rejected"

            )


        signal = generate_signal(

            setup

        )


        if signal:

            BOT_STATE["signals"] += 1


        return signal


    except Exception as e:

        BOT_STATE["errors"] += 1

        handle_error(

            e

        )

        return None



# ==========================
# BOT PROCESS CYCLE
# ==========================
def bot_cycle():

    try:

        # ==========================
        # MARKET DATA
        # ==========================

        data = get_market_data()


        if not validate_market_data(

            data

        ):

            return None



        # ==========================
        # SCANNER
        # ==========================

        scan_result = run_scanner(

            data

        )


        if not scan_result:

            return None



        # ==========================
        # MARKET BIAS
        # ==========================

        bias = prepare_market_bias(

            data

        )



        # ==========================
        # COMBINE SETUP
        # ==========================

        setup = {

            "scan":

            scan_result,

            "bias":

            bias

        }



        # ==========================
        # SIGNAL PROCESS
        # ==========================

        signal = process_signal(

            setup

        )


        return signal



    except Exception as e:

        BOT_STATE["errors"] += 1

        handle_error(

            e

        )

        return None

# ==========================
# TELEGRAM SENDER
# ==========================

def send_signal_telegram(

    signal

):

    try:

        from telegram_bot import send_message


        message = signal_text(

            signal

        )


        send_message(

            message

        )


        return True


    except Exception as e:

        handle_error(

            e

        )

        return False



# ==========================
# NOTIFICATION SYSTEM
# ==========================

def notify_signal(

    signal

):

    if signal is None:

        return False


    if signal["direction"] == "NO TRADE":

        return False


    return send_signal_telegram(

        signal

    )



# ==========================
# SIGNAL PIPELINE FINAL
# ==========================

def final_signal_process(

    setup

):

    signal = process_signal(

        setup

    )


    notify_signal(

        signal

    )


    return signal 
# ==========================
# MAIN BOT LOOP
# ==========================

def run_bot():

    start_bot()


    while BOT_STATE["running"]:

        try:

            signal = bot_cycle()


            if signal:

                notify_signal(

                    signal

                )


            time.sleep(

                60

            )


        except Exception as e:

            BOT_STATE["errors"] += 1

            handle_error(

                e

            )


            time.sleep(

                10

            )



# ==========================
# STOP BOT
# ==========================

def stop_bot():

    BOT_STATE["running"] = False


    trade_log(

        "BOT V5 Stopped"

    )


    return True



# ==========================
# BOT STATUS
# ==========================

def bot_status():

    return {

        "running":

        BOT_STATE["running"],

        "signals":

        BOT_STATE["signals"],

        "errors":

        BOT_STATE["errors"]

    } 
# ==========================
# MAIN ENGINE
# ==========================

def main_engine():

    try:

        signal = bot_cycle()


        if signal:

            notify_signal(

                signal

            )


        return signal


    except Exception as e:

        handle_error(

            e

        )

        return None



# ==========================
# MAIN ENGINE V5
# ==========================

def main_engine_v5():

    start_bot()


    result = main_engine()


    return {

        "status":

        bot_status(),

        "signal":

        result

    }



# ==========================
# TEST MODE
# ==========================

def test_mode():

    reset_bot()


    return main_engine_v5() 

# ==========================
# FINAL STATUS
# ==========================

def final_status():

    return {

        "bot":

        BOT_STATE["running"],

        "signals":

        BOT_STATE["signals"],

        "errors":

        BOT_STATE["errors"]

    }


# ==========================
# MODULE REPORT
# ==========================

def module_report():

    return {

        "bot_status":

        bot_status(),

        "utils":

        utils_status(),

        "trend":

        trend_status(),

        "session":

        session_status(),

        "signal":

        signal_status()

    }



# ==========================
# PRODUCTION CHECK
# ==========================

def production_check():

    checks = [

        final_utils_check(),

        final_session_check(),

        True

    ]


    return all(

        checks

    ) 
# ==========================
# MAIN RUNNER
# ==========================

def run():

    try:

        start_bot()


        trade_log(

            "MAIN V5 Running"

        )


        run_bot()


    except KeyboardInterrupt:

        stop_bot()



    except Exception as e:

        handle_error(

            e

        )

        stop_bot()



# ==========================
# EXPORTS
# ==========================

__all__ = [

    "reset_bot",

    "start_bot",

    "get_market_data",

    "validate_market_data",

    "market_check",

    "check_market_trend",

    "check_market_session",

    "prepare_market_bias",

    "run_scanner",

    "run_filters",

    "generate_signal",

    "process_signal",

    "bot_cycle",

    "send_signal_telegram",

    "notify_signal",

    "final_signal_process",

    "run_bot",

    "stop_bot",

    "bot_status",

    "main_engine",

    "main_engine_v5",

    "test_mode",

    "final_status",

    "module_report",

    "production_check",

    "run"

]



# ==========================
# START
# ==========================

if __name__ == "__main__":

    result = test_mode()

    print(result)
