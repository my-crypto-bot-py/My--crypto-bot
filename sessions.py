from datetime import datetime, timezone


# ==========================
# SESSION ENGINE V5
# ==========================

SESSION_STATE = {

    "current": "NONE",

    "active": False,

    "allowed": False

}


# ==========================
# SESSION TIMES (UTC)
# ==========================

SESSIONS = {

    "ASIA": {

        "start": 0,

        "end": 8

    },

    "LONDON": {

        "start": 7,

        "end": 16

    },

    "NEW_YORK": {

        "start": 13,

        "end": 21

    }

}



# ==========================
# GET UTC HOUR
# ==========================

def get_utc_hour():

    return datetime.now(

        timezone.utc

    ).hour



# ==========================
# CHECK SESSION
# ==========================

def check_session():

    hour = get_utc_hour()


    for name, session in SESSIONS.items():

        if session["start"] <= hour < session["end"]:

            return name


    return "NONE"
    # ==========================
# ACTIVE SESSION CHECK
# ==========================

def is_session_active():

    current = check_session()


    if current != "NONE":

        return True


    return False



# ==========================
# UPDATE SESSION STATE
# ==========================

def update_session_state():

    current = check_session()


    SESSION_STATE["current"] = current

    SESSION_STATE["active"] = (

        current != "NONE"

    )

    SESSION_STATE["allowed"] = (

        current in [

            "LONDON",

            "NEW_YORK"

        ]

    )


    return SESSION_STATE



# ==========================
# SESSION FILTER
# ==========================

def session_filter():

    state = update_session_state()


    return state["allowed"]
    # ==========================
# SESSION STRENGTH
# ==========================

def session_strength(

    session

):

    if session == "LONDON":

        return "HIGH"


    if session == "NEW_YORK":

        return "HIGH"


    if session == "ASIA":

        return "MEDIUM"


    return "LOW"



# ==========================
# BEST SESSION CHECK
# ==========================

def best_trading_session():

    current = check_session()


    return current in [

        "LONDON",

        "NEW_YORK"

    ]



# ==========================
# SESSION SCORE
# ==========================

def session_score():

    current = check_session()


    if current in [

        "LONDON",

        "NEW_YORK"

    ]:

        return 10


    elif current == "ASIA":

        return 5


    return 0
    # ==========================
# SESSION REPORT
# ==========================

def session_report():

    state = update_session_state()


    return {

        "session":

        state["current"],

        "active":

        state["active"],

        "allowed":

        state["allowed"],

        "strength":

        session_strength(

            state["current"]

        ),

        "score":

        session_score()

    }



# ==========================
# DEBUG SESSION
# ==========================

def debug_session():

    report = session_report()


    print("\n========== SESSION V5 ==========")

    print(

        "Current :",

        report["session"]

    )

    print(

        "Active :",

        report["active"]

    )

    print(

        "Allowed :",

        report["allowed"]

    )

    print(

        "Strength :",

        report["strength"]

    )

    print(

        "Score :",

        report["score"]

    )

    print(

        "================================\n"

    )


    return report



# ==========================
# SCANNER SESSION CHECK
# ==========================

def session_for_scanner():

    report = session_report()


    return {

        "allowed":

        report["allowed"],

        "score":

        report["score"],

        "session":

        report["session"]

    }
    # ==========================
# SESSION VALIDATION
# ==========================

def validate_session():

    report = session_report()


    return report["allowed"]



# ==========================
# SESSION DIRECTION
# ==========================

def session_direction():

    current = check_session()


    if current == "LONDON":

        return "ACTIVE"



    if current == "NEW_YORK":

        return "ACTIVE"



    if current == "ASIA":

        return "ACTIVE"



    return "INACTIVE"



# ==========================
# SESSION CONFIDENCE BONUS
# ==========================

def session_confidence_bonus():

    score = session_score()


    if score >= 10:

        return 10


    elif score >= 5:

        return 5


    return 0
    # ==========================
# SESSION FILTER ENGINE
# ==========================

def session_filter_engine():

    report = session_report()


    return {

        "approved":

        report["allowed"],

        "session":

        report["session"],

        "score":

        report["score"]

    }



# ==========================
# TRADE SESSION APPROVAL
# ==========================

def approve_session_trade():

    result = session_filter_engine()


    return result["approved"]



# ==========================
# ADVANCED SESSION CHECK
# ==========================

def advanced_session_check(

    require_high_session=True

):

    report = session_report()


    if not report["active"]:

        return False


    if require_high_session:

        return report["strength"] == "HIGH"


    return True
    # ==========================
# ENGINE STATUS
# ==========================

def session_status():

    state = update_session_state()


    return {

        "current":

        state["current"],

        "active":

        state["active"],

        "allowed":

        state["allowed"]

    }



# ==========================
# MODULE REPORT
# ==========================

def session_module_report():

    return {

        "status":

        session_status(),

        "report":

        session_report()

    }



# ==========================
# FINAL SESSION CHECK
# ==========================

def final_session_check():

    return approve_session_trade()
    # ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def sessions_engine():

    report = session_module_report()


    return {

        "session":

        report["report"],

        "ready":

        report["status"]["allowed"]

    }



# ==========================
# SESSIONS ENGINE V5
# ==========================

def sessions_engine_v5():

    result = sessions_engine()


    return {

        "current":

        result["session"]["session"],

        "active":

        result["session"]["active"],

        "allowed":

        result["ready"],

        "score":

        result["session"]["score"]

    }



# ==========================
# TEST ENGINE
# ==========================

def test_sessions():

    return sessions_engine_v5()
    # ==========================
# RESET SESSION
# ==========================

def reset_session():

    SESSION_STATE["current"] = "NONE"

    SESSION_STATE["active"] = False

    SESSION_STATE["allowed"] = False


    return True



# ==========================
# FINAL DEBUG
# ==========================

def final_session_debug():

    report = session_report()


    print("\n========== FINAL SESSION V5 ==========")

    print("Session :", report["session"])

    print("Active :", report["active"])

    print("Allowed :", report["allowed"])

    print("Strength :", report["strength"])

    print("Score :", report["score"])

    print("======================================\n")


    return report



# ==========================
# SESSION SUMMARY
# ==========================

def session_summary():

    report = session_report()


    return {

        "session":

        report["session"],

        "score":

        report["score"],

        "trade_allowed":

        report["allowed"]

    }
    # ==========================
# EXPORTS
# ==========================

__all__ = [

    "check_session",

    "get_utc_hour",

    "is_session_active",

    "update_session_state",

    "session_filter",

    "session_strength",

    "best_trading_session",

    "session_score",

    "session_report",

    "debug_session",

    "session_for_scanner",

    "validate_session",

    "session_direction",

    "session_confidence_bonus",

    "session_filter_engine",

    "approve_session_trade",

    "advanced_session_check",

    "session_status",

    "session_module_report",

    "final_session_check",

    "sessions_engine",

    "sessions_engine_v5",

    "test_sessions",

    "reset_session",

    "final_session_debug",

    "session_summary"

]
