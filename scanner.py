import pandas as pd
import numpy as np
import time


# ==========================
# ICT SCANNER ENGINE V5
# ==========================


# ==========================
# SETTINGS
# ==========================

SYMBOLS = [

    "BTC-USDT-SWAP",

    "ETH-USDT-SWAP",

    "SOL-USDT-SWAP",

    "XRP-USDT-SWAP"

]


TIMEFRAME = "5m"

MAX_RESULTS = 5



# ==========================
# SCANNER STATE
# ==========================

scanner_state = {

    "scanned": 0,

    "signals": [],

    "last_scan": None

}



# ==========================
# DATA PREPARE
# ==========================

def prepare_scan_data(df):

    df = df.copy()


    numeric = [

        "open",

        "high",

        "low",

        "close",

        "volume"

    ]


    for col in numeric:

        df[col] = pd.to_numeric(

            df[col],

            errors="coerce"

        )


    df.dropna(

        inplace=True

    )


    df.reset_index(

        drop=True,

        inplace=True

    )


    return df



# ==========================
# SYMBOL OBJECT
# ==========================

def create_symbol_object(

    symbol,

    df

):

    return {

        "symbol": symbol,

        "data": df,

        "timeframe": TIMEFRAME,

        "time": time.time()

    }
# ==========================
# MARKET DATA STORAGE
# ==========================

market_data_store = {}



# ==========================
# ADD MARKET DATA
# ==========================

def add_market_data(

    symbol,

    df

):

    if df is None:

        return False


    prepared = prepare_scan_data(

        df

    )


    market_data_store[symbol] = create_symbol_object(

        symbol,

        prepared

    )


    return True



# ==========================
# GET MARKET DATA
# ==========================

def get_market_data(

    symbol

):

    return market_data_store.get(

        symbol

    )



# ==========================
# SCAN SYMBOL LIST
# ==========================
def scan_symbols():

    results = []


    for symbol in SYMBOLS:

        data = get_market_data(

            symbol,

            TIMEFRAME,

            300

        )


        if data is not None and not data.empty:

            print("DATA RECEIVED:", symbol, len(data))

            results.append(

                {

                    "symbol": symbol,

                    "data": data

                }

            )


        else:

            print("NO DATA:", symbol)


        scanner_state["scanned"] += 1


    scanner_state["last_scan"] = time.time()

    print("TOTAL SYMBOLS:", len(results))


    return results
# ==========================
# MODULE CONNECTION
# ==========================

def import_engines():

    try:

        from confidence import (

            confidence_engine_v5

        )


        from risk import (

            risk_engine_v5

        )


        return {

            "confidence":

            confidence_engine_v5,

            "risk":

            risk_engine_v5

        }


    except Exception as e:

        return {

            "error":

            str(e)

        }



# ==========================
# SIGNAL ANALYZER
# ==========================

def analyze_symbol(

    symbol_data,

    modules

):

    if symbol_data is None:

        return None


    df = symbol_data["data"]


    # Placeholder data containers

    market = {}

    structure = {}

    smart_money = {}

    pd_array = {}

    ote = {}

    smt = {}


    confidence = modules["confidence"](

        market,

        structure,

        smart_money,

        pd_array,

        ote,

        smt

    )


    return {

        "symbol":

        symbol_data["symbol"],

        "confidence":

        confidence

    }
# ==========================
# MARKET SCAN ENGINE
# ==========================
def run_market_scan():

    print("SCANNER RUNNING")

    try:

        modules = import_engines()

        print("MODULES:", modules)

        if "error" in modules:

            return {
                "error": modules["error"]
            }

        results = []

        symbols = scan_symbols()

        print("SYMBOLS FOUND:", symbols)

        for symbol_data in symbols:

            result = analyze_symbol(
                symbol_data,
                modules
            )

            print("ANALYSIS RESULT:", result)

            if result:

                results.append(result)

        scanner_state["signals"] = results

        print("FINAL SIGNALS:", results)

        return results

    except Exception as e:

        print("RUN MARKET SCAN ERROR:", e)

        raise


# ==========================
# FILTER SETUPS
# ==========================

def filter_setups(

    results

):

    setups = []


    for item in results:

        confidence = item.get(

            "confidence",

            {}

        )


        if confidence.get(

            "signal"

        ) == "TRADE":

            setups.append(

                item

            )


    return setups



# ==========================
# BEST SETUP
# ==========================

def get_best_setup(

    results

):

    if not results:

        return None


    return max(

        results,

        key=lambda x:

        x["confidence"].get(

            "confidence",

            0

        )

    )
    # ==========================
# SIGNAL BUILDER
# ==========================

def build_signal(

    setup

):

    if setup is None:

        return None


    confidence = setup.get(

        "confidence",

        {}

    )


    direction = confidence.get(

        "direction",

        "NO TRADE"

    )


    if direction == "NO TRADE":

        return None


    return {

        "symbol":

        setup["symbol"],

        "direction":

        direction,

        "confidence":

        confidence.get(

            "confidence",

            0

        ),

        "status":

        "READY"

    }



# ==========================
# ENTRY PREPARATION
# ==========================

def prepare_signal(

    setup,

    entry,

    sl,

    tp

):

    signal = build_signal(

        setup

    )


    if signal is None:

        return None


    signal.update(

        {

            "entry":

            entry,

            "sl":

            sl,

            "tp":

            tp

        }

    )


    return signal



# ==========================
# RISK CONNECTION
# ==========================

def validate_setup_risk(

    signal,

    balance,

    leverage=1

):

    if signal is None:

        return False


    modules = import_engines()


    risk = modules["risk"](

        balance,

        signal["entry"],

        signal["sl"],

        signal["tp"],

        leverage,

        signal["confidence"]

    )


    return risk["permission"]
    # ==========================
# FINAL SCANNER PIPELINE
# ==========================

def scanner_pipeline():

    results = run_market_scan()


    if not results:

        return None


    setups = filter_setups(

        results

    )


    if not setups:

        return {

            "signal":

            None,

            "reason":

            "No valid setup"

        }


    best = get_best_setup(

        setups

    )


    signal = build_signal(

        best

    )


    return {

        "signal":

        signal,

        "setup":

        best

    }



# ==========================
# AUTO SIGNAL GENERATOR
# ==========================

def generate_signal():

    result = scanner_pipeline()


    if result is None:

        return None


    return result.get(

        "signal"

    )



# ==========================
# SCAN STATUS
# ==========================

def scan_status():

    return {

        "scanned":

        scanner_state["scanned"],

        "signals":

        len(scanner_state["signals"]),

        "last_scan":

        scanner_state["last_scan"]

    }
    # ==========================
# MULTI TIMEFRAME CHECK
# ==========================

def timeframe_confirmation(

    htf_data,

    ltf_data

):

    if htf_data is None or ltf_data is None:

        return False


    htf_trend = htf_data.get(

        "trend"

    )


    ltf_trend = ltf_data.get(

        "trend"

    )


    return (

        htf_trend

        ==

        ltf_trend

    )



# ==========================
# BTC CORRELATION CHECK
# ==========================

def btc_confirmation(

    btc_data,

    asset_data

):

    if btc_data is None or asset_data is None:

        return False


    btc_direction = btc_data.get(

        "direction"

    )


    asset_direction = asset_data.get(

        "direction"

    )


    return (

        btc_direction

        ==

        asset_direction

    )



# ==========================
# ADVANCED FILTER
# ==========================

def advanced_filter(

    setup,

    htf=None,

    ltf=None,

    btc=None

):

    if setup is None:

        return False


    if htf and ltf:

        if not timeframe_confirmation(

            htf,

            ltf

        ):

            return False


    if btc:

        if not btc_confirmation(

            btc,

            setup

        ):

            return False


    return True
    # ==========================
# SIGNAL RANKING
# ==========================

def rank_signals(

    signals

):

    if not signals:

        return []


    ranked = sorted(

        signals,

        key=lambda x:

        x.get(

            "confidence",

            0

        ),

        reverse=True

    )


    return ranked



# ==========================
# TOP SIGNAL
# ==========================

def get_top_signal(

    signals

):

    ranked = rank_signals(

        signals

    )


    if not ranked:

        return None


    return ranked[0]



# ==========================
# SCANNER REPORT
# ==========================

def scanner_report():

    signals = scanner_state["signals"]


    ranked = rank_signals(

        signals

    )


    return {

        "total_scanned":

        scanner_state["scanned"],

        "total_signals":

        len(signals),

        "top_signal":

        get_top_signal(

            ranked

        ),

        "last_scan":

        scanner_state["last_scan"]

    }
    # ==========================
# SCANNER DEBUG PANEL
# ==========================

def debug_scanner():

    report = scanner_report()


    print("\n========== SCANNER V5 ==========")

    print(

        "Scanned :",

        report["total_scanned"]

    )

    print(

        "Signals :",

        report["total_signals"]

    )

    print(

        "Top     :",

        report["top_signal"]

    )

    print(

        "Last    :",

        report["last_scan"]

    )

    print(

        "================================\n"

    )


    return report



# ==========================
# RESET SCANNER
# ==========================

def reset_scanner():

    scanner_state["scanned"] = 0

    scanner_state["signals"] = []

    scanner_state["last_scan"] = None


    market_data_store.clear()


    return True



# ==========================
# TEST SCAN
# ==========================

def test_scan(symbol):

    data = get_market_data(

        symbol

    )


    if data is None:

        return {

            "status":

            "NO DATA"

        }


    return {

        "status":

        "READY",

        "symbol":

        symbol,

        "candles":

        len(data["data"])

    }
    # ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def scanner_engine_v5():

    result = scanner_pipeline()


    if result is None:

        return {

            "signal":

            None,

            "status":

            "FAILED"

        }


    return {

        "signal":

        result.get("signal"),

        "setup":

        result.get("setup"),

        "status":

        "COMPLETED"

    }



# ==========================
# FINAL SCANNER RUN
# ==========================

def run_scanner(

    market_data

):

    try:

        from scanner import run_market_scan

        result = run_market_scan()

        return result

    except Exception as e:

        print("RUN SCANNER ERROR:", e)

        handle_error(e)

        return None



# ==========================
# EXPORTS
# ==========================

__all__ = [

    "add_market_data",

    "get_market_data",

    "scan_symbols",

    "run_market_scan",

    "filter_setups",

    "get_best_setup",

    "scanner_pipeline",

    "generate_signal",

    "scanner_engine_v5",

    "run_scanner",

    "scanner_report",

    "debug_scanner",

    "reset_scanner"

]
