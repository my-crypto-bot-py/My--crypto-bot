import datetime
import math
import traceback
import logging

# ==========================
# UTILS ENGINE V5
# ==========================

UTILS_STATE = {

    "errors": 0,

    "last_error": None

}



# ==========================
# TIME FUNCTION
# ==========================

def current_time():

    return datetime.datetime.now()



# ==========================
# UTC TIME
# ==========================

def current_utc():

    return datetime.datetime.utcnow()



# ==========================
# RESET UTILS
# ==========================

def reset_utils():

    UTILS_STATE["errors"] = 0

    UTILS_STATE["last_error"] = None


    return True
  # ==========================
# PRICE ROUNDING
# ==========================

def round_price(

    price,

    decimals=2

):

    return round(

        float(price),

        decimals

    )



# ==========================
# NUMBER FORMAT
# ==========================

def format_number(

    number

):

    try:

        return f"{float(number):,.2f}"


    except:

        return "0.00"



# ==========================
# SAFE FLOAT
# ==========================

def safe_float(

    value,

    default=0.0

):

    try:

        return float(value)


    except:

        return default



# ==========================
# SAFE INT
# ==========================

def safe_int(

    value,

    default=0

):

    try:

        return int(value)


    except:

        return default
      # ==========================
# ERROR HANDLER
# ==========================

def handle_error(

    error

):

    UTILS_STATE["errors"] += 1

    UTILS_STATE["last_error"] = str(

        error

    )


    return {

        "error":

        True,

        "message":

        str(error)

    }



# ==========================
# EXCEPTION LOGGER
# ==========================

def log_exception():

    error = traceback.format_exc()


    UTILS_STATE["errors"] += 1

    UTILS_STATE["last_error"] = error


    return error



# ==========================
# DEBUG HELPER
# ==========================

def debug_message(

    message

):

    print(

        "[DEBUG]",

        message

    )


    return True
  # ==========================
# EMPTY DATA CHECK
# ==========================

def is_empty(

    data

):

    if data is None:

        return True


    try:

        return len(data) == 0


    except:

        return False



# ==========================
# DATA VALIDATION
# ==========================

def validate_data(

    data

):

    if is_empty(

        data

    ):

        return False


    return True



# ==========================
# COLUMN VALIDATION
# ==========================

def validate_columns(

    df,

    columns

):

    for col in columns:

        if col not in df.columns:

            return False


    return True
  


# ==========================
# LOGGING SETUP
# ==========================

def setup_logger(

    name="BOT_V5"

):

    logger = logging.getLogger(

        name

    )


    if not logger.handlers:

        handler = logging.StreamHandler()

        formatter = logging.Formatter(

            "%(asctime)s - %(levelname)s - %(message)s"

        )

        handler.setFormatter(

            formatter

        )

        logger.addHandler(

            handler

        )


    logger.setLevel(

        logging.INFO

    )


    return logger



# ==========================
# TRADE LOG HELPER
# ==========================

def trade_log(

    message

):

    logger = setup_logger()


    logger.info(

        message

    )


    return True



# ==========================
# ERROR LOG HELPER
# ==========================

def error_log(

    message

):

    logger = setup_logger()


    logger.error(

        message

    )


    return True
  import json


# ==========================
# DICTIONARY HELPER
# ==========================

def get_value(

    data,

    key,

    default=None

):

    try:

        return data.get(

            key,

            default

        )


    except:

        return default



# ==========================
# UPDATE DICTIONARY
# ==========================

def update_dict(

    data,

    key,

    value

):

    data[key] = value


    return data



# ==========================
# JSON SAVE
# ==========================

def save_json(

    file,

    data

):

    try:

        with open(

            file,

            "w"

        ) as f:

            json.dump(

                data,

                f,

                indent=4

            )


        return True


    except Exception as e:

        handle_error(

            e

        )

        return False



# ==========================
# JSON LOAD
# ==========================

def load_json(

    file

):

    try:

        with open(

            file,

            "r"

        ) as f:

            return json.load(

                f

            )


    except:

        return {}
      import time


# ==========================
# RETRY SYSTEM
# ==========================

def retry_action(

    function,

    retries=3,

    delay=2

):

    for attempt in range(

        retries

    ):

        try:

            return function()


        except Exception as e:

            handle_error(

                e

            )


            time.sleep(

                delay

            )


    return None



# ==========================
# SAFE EXECUTION
# ==========================

def safe_execute(

    function,

    *args,

    **kwargs

):

    try:

        return function(

            *args,

            **kwargs

        )


    except Exception as e:

        handle_error(

            e

        )

        return None



# ==========================
# API ERROR HANDLER
# ==========================

def api_error(

    response

):

    if response is None:

        return True


    if hasattr(

        response,

        "status_code"

    ):

        return response.status_code >= 400


    return False
# ==========================
# UTILS ENGINE
# ==========================

def utils_engine():

    return {

        "errors":

        UTILS_STATE["errors"],

        "last_error":

        UTILS_STATE["last_error"]

    }



# ==========================
# UTILS ENGINE V5
# ==========================

def utils_engine_v5():

    result = utils_engine()


    return {

        "status":

        "READY",

        "errors":

        result["errors"],

        "last_error":

        result["last_error"]

    }



# ==========================
# TEST ENGINE
# ==========================

def test_utils():

    return utils_engine_v5()
# ==========================
# UTILS STATUS
# ==========================

def utils_status():

    return {

        "errors":

        UTILS_STATE["errors"],

        "last_error":

        UTILS_STATE["last_error"]

    }



# ==========================
# MODULE REPORT
# ==========================

def utils_module_report():

    return {

        "status":

        utils_status(),

        "engine":

        utils_engine_v5()

    }



# ==========================
# FINAL UTILS CHECK
# ==========================

def final_utils_check():

    return (

        UTILS_STATE["errors"]

        ==

        0

    )
# ==========================
# EXPORTS
# ==========================

__all__ = [

    "current_time",

    "current_utc",

    "reset_utils",

    "round_price",

    "format_number",

    "safe_float",

    "safe_int",

    "handle_error",

    "log_exception",

    "debug_message",

    "is_empty",

    "validate_data",

    "validate_columns",

    "setup_logger",

    "trade_log",

    "error_log",

    "get_value",

    "update_dict",

    "save_json",

    "load_json",

    "retry_action",

    "safe_execute",

    "api_error",

    "utils_engine",

    "utils_engine_v5",

    "test_utils",

    "utils_status",

    "utils_module_report",

    "final_utils_check"

]
