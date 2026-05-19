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


# Attack burst detection (failed login spike kroz vreme)
def attack_burst_detection(threshold=5):
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
                "_id": {
                    "$dateTrunc": {
                        "date": "$timestamp",
                        "unit": "minute",
                        "binSize": 5
                    }
                },
                "count": {"$sum": 1}
            }
        },
        {
            "$match": {
                "count": {"$gte": threshold}
            }
        },
        {
            "$sort": {
                "_id": 1
            }
        }
    ]

    return list(events_collection.aggregate(pipeline))


# Trend aktivnosti kroz vreme
def events_trend():
    start, end = get_time_range()

    pipeline = [
        {
            "$match": {
                "timestamp": {"$gte": start, "$lte": end}
            }
        },
        {
            "$group": {
                "_id": {
                    "$dateTrunc": {
                        "date": "$timestamp",
                        "unit": "minute",
                        "binSize": 5
                    }
                },
                "count": {"$sum": 1}
            }
        },
        {
            "$sort": {
                "_id": 1
            }
        }
    ]

    return list(events_collection.aggregate(pipeline))


# Suspicious user activity score
def suspicious_users():
    start, end = get_time_range()

    pipeline = [
        {
            "$match": {
                "timestamp": {
                    "$gte": start,
                    "$lte": end
                }
            }
        },
        {
            "$group": {
                "_id": "$user",

                "failed_logins": {
                    "$sum": {
                        "$cond": [
                            {"$eq": ["$type", "failed_login"]},
                            1,
                            0
                        ]
                    }
                },

                "unique_ips": {
                    "$addToSet": "$ip"
                }
            }
        },
        {
            "$project": {
                "failed_logins": 1,

                "ip_count": {
                    "$size": "$unique_ips"
                },

                "risk_score": {
                    "$add": [
                        {"$multiply": ["$failed_logins", 2]},
                        {
                            "$cond": [
                                {
                                    "$gte": [
                                        {"$size": "$unique_ips"},
                                        3
                                    ]
                                },
                                3,
                                0
                            ]
                        }
                    ]
                }
            }
        },
        {
            "$sort": {
                "risk_score": -1
            }
        }
    ]

    return list(events_collection.aggregate(pipeline))