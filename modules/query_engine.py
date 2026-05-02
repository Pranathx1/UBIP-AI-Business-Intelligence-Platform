import pandas as pd

def process_query(query, events):
    query = query.lower()
    events["date"] = pd.to_datetime(events["date"])

    response = {
        "type": "text",
        "title": "Query Result",
        "data": None
    }

    # ---------------- NO INSPECTION ----------------
    if "no inspection" in query or "without inspection" in query:
        last_inspection = events[events["event"] == "inspection"].groupby("ubid")["date"].max()
        now = pd.Timestamp.now()

        result = []
        for ubid, date in last_inspection.items():
            if (now - date).days > 365:
                result.append({"UBID": ubid, "Last Inspection": date})

        response["type"] = "table"
        response["title"] = "Businesses without inspection in last 12 months"
        response["data"] = pd.DataFrame(result)

    # ---------------- DORMANT ----------------
    elif "dormant" in query or "inactive" in query:
        last_activity = events.groupby("ubid")["date"].max()
        now = pd.Timestamp.now()

        result = []
        for ubid, date in last_activity.items():
            if (now - date).days > 180:
                result.append({"UBID": ubid, "Last Activity": date})

        response["type"] = "table"
        response["title"] = "Dormant / Inactive Businesses"
        response["data"] = pd.DataFrame(result)

    # ---------------- RECENT ACTIVITY ----------------
    elif "recent" in query or "active" in query:
        last_activity = events.groupby("ubid")["date"].max()

        result = []
        for ubid, date in last_activity.items():
            result.append({"UBID": ubid, "Last Activity": date})

        response["type"] = "table"
        response["title"] = "Businesses with Recent Activity"
        response["data"] = pd.DataFrame(result)

    # ---------------- HIGH RISK ----------------
    elif "risk" in query:
        last_activity = events.groupby("ubid")["date"].max()
        now = pd.Timestamp.now()

        result = []
        for ubid, date in last_activity.items():
            days = (now - date).days

            if days > 365:
                risk = "High"
            elif days > 180:
                risk = "Medium"
            else:
                risk = "Low"

            if risk == "High":
                result.append({"UBID": ubid, "Risk": risk, "Last Activity": date})

        response["type"] = "table"
        response["title"] = "High Risk Businesses"
        response["data"] = pd.DataFrame(result)

    # ---------------- DEFAULT ----------------
    else:
        response["type"] = "text"
        response["title"] = "Unknown Query"
        response["data"] = "Try queries like: 'no inspection', 'inactive businesses', 'high risk', 'recent activity'"

    return response