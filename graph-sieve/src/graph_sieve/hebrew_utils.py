from bidi.algorithm import get_display

def normalize_rtl_text(text: str) -> str:
    """
    Checks for Hebrew characters and ensures logical reading order for RTL text.
    """
    # If Hebrew characters detected, ensure logical order
    if any("\u0590" <= c <= "\u05FF" for c in text):
        return get_display(text)
    return text
