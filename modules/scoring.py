def classify_confidence(score):
    if score > 0.85:
        return "Auto Linked"
    elif score > 0.6:
        return "Needs Review"
    else:
        return "Rejected"