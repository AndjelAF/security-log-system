from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["security_logs"]

if "events" not in db.list_collection_names():
    db.create_collection(
        "events",
        timeseries={
            "timeField": "timestamp",
            "metaField": "user",
            "granularity": "seconds"
        }
    )

events_collection = db["events"]