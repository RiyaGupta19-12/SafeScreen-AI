import re


def analyze_message(text):
    text_lower = text.lower()

    signals = []

    suspicious_words = [
        "urgent",
        "immediately",
        "verify",
        "otp",
        "password",
        "blocked",
        "suspended",
        "click here",
        "claim",
        "prize",
        "reward",
        "account",
        "bank",
        "refund"
    ]

    for word in suspicious_words:
        if word in text_lower:
            signals.append(f"Suspicious keyword: '{word}'")

    # Detect URLs
    urls = re.findall(r"https?://\S+|www\.\S+", text_lower)

    if urls:
        signals.append("A web link was detected.")

    # Simple risk level
    if len(signals) >= 4:
        risk = "HIGH"
    elif len(signals) >= 2:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return risk, signals