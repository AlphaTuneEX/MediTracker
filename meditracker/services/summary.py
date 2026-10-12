from collections import defaultdict

def get_daily_summary(timeline):
    summary = {
        "count" : len(timeline),
        "ingredients" : defaultdict(int),
        "last_time" : None
    }

    for event in timeline:
        ingredient = event["ingredient"]
        dose = event["dose"]
        summary["ingredients"][ingredient] += dose

        if summary["last_time"] is None or event ["time"] > summary["last_time"]:
            summary["last_time"] = event["time"]

    return summary