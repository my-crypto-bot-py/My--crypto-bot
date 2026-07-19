# ==========================
# ICT MARKET SCANNER V2
# ==========================

from config import SYMBOLS, TREND_TF, MIN_SCORE

from market import (
    get_market_data,
    detect_trend,
    detect_volume_confirmation
)



# ==========================
# SCAN ALL SYMBOLS
# ==========================

def scan_market():

    results = []


    for symbol in SYMBOLS:


        try:


            df = get_market_data(

                symbol,

                TREND_TF,

                300

            )



            if df is None or df.empty:

                continue




            trend_data = detect_trend(

                df

            )



            trend = trend_data["trend"]

            strength = trend_data["strength"]




            # Skip weak trend

            if trend == "SIDEWAYS":

                continue



            volume = detect_volume_confirmation(

                df

            )



            # Volume bonus

            if volume:

                strength += 5




            strength = min(

                strength,

                100

            )



            if strength < MIN_SCORE:
    
                    continue

            




            results.append({

                "symbol":

                symbol,


                "trend":

                trend,


                "strength":

                strength,


                "volume":

                volume

            })



        except Exception as e:


            print(

                "Scanner Error",

                symbol,

                e

            )




    results.sort(

        key=lambda x:

        x["strength"],

        reverse=True

    )



    return results





# ==========================
# BEST SYMBOL
# ==========================

def get_best_symbol():


    data = scan_market()



    if not data:

        return None




    print(

        "\n========== ICT SCANNER =========="

    )



    for coin in data:


        print(

            coin["symbol"],

            coin["trend"],

            coin["strength"],

            "Volume:",

            coin["volume"]

        )



    print(

        "================================\n"

    )



    return data[0]
