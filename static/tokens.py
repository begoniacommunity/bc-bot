TELEGRAM_TOKEN = ""
EXCHANGERATES_TOKEN = ""

if __name__ != "__main__" and (TELEGRAM_TOKEN == "" or EXCHANGERATES_TOKEN == ""):
    raise ValueError("No valid tokens provided! Please add them to ./static/tokens.py!")