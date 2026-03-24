from typing import Literal


def detect_language(text: str) -> Literal['en', 'hi', 'ta']:
    t = text.lower()
    # heuristic detection
    if any(x in t for x in ['namaste', 'kal', 'hain', 'aap']):
        return 'hi'
    if any(x in t for x in ['vanakkam', 'enna', 'unga']):
        return 'ta'
    return 'en'
