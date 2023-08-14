import re

def preprocess_message(message: str) -> str:
    message = re.sub(r"@(\S+)", "", message)
    message = re.sub(r"\b(?:https?:\/\/|www\.)\S+\b|\b\S+\.com\S*\b", "", message)
    message = re.sub(r"(?<!\d)(\d{1,3}(?: \d{3})*(?:\.\d+)?)(?=(?:\s\d{3})*(?:\.\d+)?|\D|$)", lambda match: match.group(1).replace(" ", ""), message)
    return message
