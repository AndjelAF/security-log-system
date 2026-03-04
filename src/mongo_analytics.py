from datetime import datetime, timedelta, timezone
from db_config import events_collection


def get_time_range():
    now = datetime.now(timezone.utc)
    yesterday = now - timedelta(days=1)
    return yesterday, now


# Događaji po tipu
def events_by_type():
    start, end = get_time_range()

    pipeline = [
        {
            "$match": {
                "timestamp": {"$gte": start, "$lte": end}
            }
        },
        {
            "$group": {
                "_id": "$type",
                "count": {"$sum": 1}
            }
        },
        {"$sort": {"count": -1}}
    ]

    return list(events_collection.aggregate(pipeline))


# Brute force po username-u
def brute_force_by_user(threshold=3):
    start, end = get_time_range()

    pipeline = [
        {
            "$match": {
                "timestamp": {"$gte": start, "$lte": end},
                "type": "failed_login"
            }
        },
        {
            "$group": {
                "_id": "$user",
                "count": {"$sum": 1}
            }
        },
        {
            "$match": {
                "count": {"$gte": threshold}
            }
        }
    ]

    return list(events_collection.aggregate(pipeline))


# Brute force po IP adresi
def brute_force_by_ip(threshold=3):
    start, end = get_time_range()

    pipeline = [
        {
            "$match": {
                "timestamp": {"$gte": start, "$lte": end},
                "type": "failed_login"
            }
        },
        {
            "$group": {
                "_id": "$ip",
                "count": {"$sum": 1}
            }
        },
        {
            "$match": {
                "count": {"$gte": threshold}
            }
        }
    ]

    return list(events_collection.aggregate(pipeline))