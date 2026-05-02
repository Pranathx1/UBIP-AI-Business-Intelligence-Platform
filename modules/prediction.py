import random

def risk_score(activity_status):
    if activity_status == "Active":
        return f"Low Risk ({random.randint(10,30)}%)"
    elif activity_status == "Dormant":
        return f"Medium Risk ({random.randint(40,70)}%)"
    else:
        return f"High Risk ({random.randint(70,95)}%)"