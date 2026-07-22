import time


# ==========================
# IMPORT MODULES V12
# ==========================

from utils import *

from trend import *

from sessions import *

from signal import *

from filters import *

# V5 Scanner (Backup)
from scanner import *

# V12 Scanner
from scanner_v12 import *

# V12 Structure
from structure_v12 import (
    get_v12_master_signal_v12
)
import structure_v12
print("IMPORTED FUNCTION CODE:")
print(structure_v12.get_v12_master_signal_v12.__code__.co_firstlineno)
print(structure_v12.get_v12_master_signal_v12.__code__.co_filename)


# ==========================
# BOT STATE V12
# ==========================

BOT_STATE = {

    "running": False,

    "signals": 0,

    "errors": 0,

    "engine": "V12",

    "last_signal": None

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

        from market import get_market_data as market_fetch


        symbol = "BTC-USDT-SWAP"

        timeframe = "5m"


        data = market_fetch(

            symbol,

            timeframe,

            300

        )


        print("MARKET DATA FETCHED:", data is not None)


        return data


    except Exception as e:

        handle_error(e)

        print("MARKET FETCH ERROR:", e)

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
# V12 SCANNER ROUTER
# ==========================

def run_scanner(
        market_data
):

    try:

        from scanner_v12 import get_v12_scanner_signal


        result = get_v12_scanner_signal(
            market_data
        )


        return result


    except Exception as e:

        handle_error(e)

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
# V12 MASTER ROUTER
# ==========================
def run_v12_engine(
        market_data
):

    try:

        print("RUN V12 ENGINE START")

        print("CALLING get_v12_master_signal_v12")

        signal = get_v12_master_signal_v12(
            market_data
        )

        print("RAW V12:", signal)

        if signal is None:
            print("V12 RETURNED NONE")
            return None

        if signal.get(
            "approved",
            False
        ):

            BOT_STATE["signals"] += 1

            BOT_STATE["last_signal"] = signal

            return {

                "direction":
                    signal.get("signal"),

                "confidence":
                    signal.get("confidence", 0),

                "engine":
                    "ICT_V12"

            }

        print("V12 NOT APPROVED:", signal)

        return None

    except Exception as e:

        BOT_STATE["errors"] += 1

        print("V12 ERROR:", repr(e))

        handle_error(e)

        return None 
# ==========================
# SAFE V12 WRAPPER
# ==========================

def get_v12_master_signal_v12(df):
    try:
        result = v12_final_signal_gate_v12(df)

        if result is None:
            return {
                "approved": False,
                "signal": "NO_TRADE",
                "confidence": 0,
                "status": "WAIT",
                "engine": "SAFE_WRAPPER"
            }

        return result

    except KeyError as e:
        print("SAFE V12 KeyError:", e)
        return {
            "approved": False,
            "signal": "NO_TRADE",
            "confidence": 0,
            "status": "WAIT",
            "engine": "SAFE_WRAPPER"
        }
        
# ==========================
# BOT PROCESS CYCLE
# ==========================

def bot_cycle():

    print("BOT CYCLE RUNNING")

    try:

        data = get_market_data()

        print("MARKET DATA:", data)


        if not validate_market_data(data):

            print("MARKET DATA INVALID")

            return None


        print("MARKET DATA OK")


        # ==========================
        # V12 MASTER ENGINE
        # ==========================

        v12_signal = run_v12_engine(
            data
        )


        print(
            "V12 SIGNAL:",
            v12_signal
        )


        if v12_signal:

            return v12_signal



        # ==========================
        # FALLBACK V5 SCANNER
        # ==========================

        scan_result = run_scanner(
            data
        )


        print(
            "SCANNER RESULT:",
            scan_result
        )


        if not scan_result:

            print(
                "NO SCANNER RESULT"
            )

            return None



        bias = prepare_market_bias(
            data
        )


        setup = {

            "scan": scan_result,

            "bias": bias

        }


        signal = process_signal(
            setup
        )


        print(
            "SIGNAL:",
            signal
        )


        return signal



    except Exception as e:

        BOT_STATE["errors"] += 1

        handle_error(e)

        print(
            "ERROR:",
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

    print("MAIN ENGINE RUNNING")

    try:

        signal = bot_cycle()

        print("BOT CYCLE RESULT:", signal)


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
