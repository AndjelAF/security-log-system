from datetime import datetime, timedelta, timezone
from db_config import events_collection
import random


users = ["andjela", "marko", "ana", "petar"]


# ---------------------------------------------------
# 1. Simulacija normalne aktivnosti kroz vreme
# ---------------------------------------------------

base_time = datetime.now(timezone.utc) - timedelta(hours=1)

for minute in range(0, 60, 5):

    current_time = base_time + timedelta(minutes=minute)

    for _ in range(random.randint(2, 5)):

        log = {
            "timestamp": current_time,
            "user": random.choice(users),
            "type": random.choice([
                "login_attempt",
                "logout"
            ]),
            "success": True,
            "ip": f"192.168.1.{random.randint(1,50)}"
        }

        events_collection.insert_one(log)



# ---------------------------------------------------
# 2. Simulacija burst napada
# ---------------------------------------------------

burst_time = datetime.now(timezone.utc) - timedelta(minutes=15)

for _ in range(15):

    log = {
        "timestamp": burst_time,
        "user": random.choice(users),
        "type": "failed_login",
        "success": False,
        "ip": "192.168.100.50"
    }

    events_collection.insert_one(log)



# ---------------------------------------------------
# 3. Simulacija suspicious user-a
# ---------------------------------------------------

suspicious_user = "marko"

for i in range(8):

    log = {
        "timestamp": datetime.now(timezone.utc) - timedelta(minutes=i),

        "user": suspicious_user,

        "type": "failed_login",

        "success": False,

        "ip": f"10.0.0.{i}"
    }

    events_collection.insert_one(log)



print("Attack simulation completed.")