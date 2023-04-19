import re

from .triggers import *
    
def preprocess_message(message: str) -> str:
    message = re.sub(r'(\d)([^\d\s.,])', r'\1 \2', message)
    message = re.sub(r'([^\d\s.,])(\d)', r'\1 \2', message)
    return message