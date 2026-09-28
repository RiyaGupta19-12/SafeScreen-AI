def combined_risk(phishing_probability, rule_risk):
    if phishing_probability >= 0.8 or rule_risk == "HIGH":
        return "HIGH"
    elif phishing_probability >= 0.5:
        return "MEDIUM"
    else:
        return "LOW"