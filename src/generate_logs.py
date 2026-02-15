import random
from datetime import datetime, timezone
from db_config import events_collection

# Nasumični korisnici i tipovi događaja
users = ["andjela", "marko", "ana", "petar"]
event_types = ["login_attempt", "failed_login", "logout"]

# Broj logova koje želimo generisati
num_logs = 50

for _ in range(num_logs):
    log = {
        "timestamp": datetime.now(timezone.utc),
        "user": random.choice(users),
        "type": random.choice(event_types),
        "success": random.choice([True, False]),
        "ip": f"192.168.{random.randint(0,255)}.{random.randint(1,254)}"
    }
    events_collection.insert_one(log)

print(f"{num_logs} logova ubačeno u kolekciju 'events'.")
