from db_config import events_collection
from collections import Counter
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# ---- 1. Funkcija za filtriranje logova ----
def filter_logs(logs, user=None, event_type=None, start_time=None, end_time=None):
    """
    Filtrira listu logova po korisniku, tipu događaja i vremenskom opsegu.
    """
    filtered = []
    for log in logs:
        ts = log["timestamp"]
        if start_time and ts < start_time:
            continue
        if end_time and ts > end_time:
            continue
        if user and log["user"] != user:
            continue
        if event_type and log["type"] != event_type:
            continue
        filtered.append(log)
    return filtered

# ---- 2. Učitaj sve logove iz baze ----
all_logs = list(events_collection.find())

# ---- 3. Primer: filtriranje logova poslednjih 24h ----
now = datetime.utcnow()           # offset-naive
yesterday = now - timedelta(days=1)
recent_logs = filter_logs(all_logs, start_time=yesterday, end_time=now)

# ---- 4. Statistika ----
type_count = Counter([log["type"] for log in recent_logs])
user_count = Counter([log["user"] for log in recent_logs])
hour_count = Counter([log["timestamp"].hour for log in recent_logs])

# ---- 5. Filter primer: failed logins po korisniku "ana" ----
failed_ana = filter_logs(recent_logs, user="ana", event_type="failed_login")
print(f"\nBroj failed_login događaja za korisnika 'ana': {len(failed_ana)}")

# ---- 6. Objedinjena vizualizacija ----
fig, axes = plt.subplots(1, 3, figsize=(18, 5))  # 1 red, 3 kolone

# Tip događaja
axes[0].bar(type_count.keys(), type_count.values(), color='skyblue')
axes[0].set_title("Broj događaja po tipu")
axes[0].set_ylabel("Broj događaja")

# Korisnici
axes[1].bar(user_count.keys(), user_count.values(), color='salmon')
axes[1].set_title("Broj događaja po korisniku")

# Po satu
axes[2].bar([str(h)+":00" for h in sorted(hour_count.keys())],
            [hour_count[h] for h in sorted(hour_count.keys())],
            color='lightgreen')
axes[2].set_title("Broj događaja po satu (UTC)")

plt.tight_layout()  # da se subplot-ovi ne preklapaju
plt.show()
