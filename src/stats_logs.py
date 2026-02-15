from pymongo import MongoClient
from datetime import datetime, timedelta, timezone
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd

# --- Konfiguracija konekcije ---
client = MongoClient("mongodb://localhost:27017/")
db = client["security_logs"]  # ime baze
collection = db["events"]     # ime kolekcije

# --- Filter logova po vremenu ---
def filter_logs(logs, start_time=None, end_time=None):
    filtered = []
    for log in logs:
        ts = log["timestamp"]
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        if start_time and ts < start_time:
            continue
        if end_time and ts > end_time:
            continue
        filtered.append(log)
    return filtered

# --- Učitavanje logova ---
all_logs = list(collection.find())

# --- Definisanje vremenskog perioda (poslednjih 24h) ---
now = datetime.now(timezone.utc)
yesterday = now - timedelta(days=1)
recent_logs = filter_logs(all_logs, start_time=yesterday, end_time=now)

# --- Statistika po tipu ---
type_counts = Counter([log["type"] for log in recent_logs])
print("Broj događaja po tipu:")
for typ, count in type_counts.items():
    print(f"{typ}: {count}")

# --- Statistika po korisniku ---
user_counts = Counter([log["user"] for log in recent_logs])
print("\nBroj događaja po korisniku:")
for user, count in user_counts.items():
    print(f"{user}: {count}")

# --- Statistika po satu (UTC) ---
hour_counts = Counter([log["timestamp"].hour for log in recent_logs])
print("\nBroj događaja po satu (UTC):")
for hour, count in sorted(hour_counts.items()):
    print(f"{hour:02d}:00 - {count} događaja")

# --- Alert za sumnjive aktivnosti ---
FAILED_LOGIN_THRESHOLD = 3
failed_counts = Counter([log["user"] for log in recent_logs if log["type"] == "failed_login"])

print("\n--- Detekcija sumnjivih aktivnosti ---")
for user, count in failed_counts.items():
    if count >= FAILED_LOGIN_THRESHOLD:
        print(f"ALERT: {user} ima {count} failed login pokušaja u poslednjih 24h!")

# --- Pivot tabela po korisniku i tipu događaja ---
df = pd.DataFrame(recent_logs)
pivot = pd.pivot_table(df, index='user', columns='type', aggfunc='size', fill_value=0)

print("\nPivot tabela (broj događaja po tipu i korisniku):")
print(pivot)

# --- Vizualizacija objedinjena ---
pivot.plot(kind='bar', stacked=True, figsize=(10,6), colormap='Set2')
plt.title("Događaji po korisniku i tipu (poslednjih 24h)")
plt.ylabel("Broj događaja")
plt.xlabel("Korisnik")
plt.tight_layout()
plt.show()
