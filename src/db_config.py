from pymongo import MongoClient

# 1. Konekcija ka lokalnom MongoDB serveru
client = MongoClient("mongodb://localhost:27017")

# 2. Baza i kolekcija
db = client["security_logs"]
events_collection = db["events"]
