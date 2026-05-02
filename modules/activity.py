import pandas as pd

def classify_activity(events_df, ubid):
    data = events_df[events_df['ubid'] == ubid]

    if len(data) == 0:
        return "Closed"

    recent = pd.to_datetime(data['date']).max()

    if (pd.Timestamp.now() - recent).days < 180:
        return "Active"
    else:
        return "Dormant"