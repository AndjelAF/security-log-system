Security Log System

Kroz ovaj projekat demonstriram primenu MongoDB Time-Series kolekcije za skladištenje i analizu sigurnosnih log podataka.

Sistem:
-generiše log događaje (login, failed_login, logout)
-skladišti ih u MongoDB time-series kolekciju
-koristi aggregation pipeline za analitiku
-prikazuje rezultate kroz Flask web aplikaciju


Korišćene tehnologije:
-Python 3
-Flask
-MongoDB (Time-Series kolekcija)
-PyMongo
-HTML + JavaScript
-Virtual Environment (venv)

Preduslovi za pokretanje
Potrebno je imati instalirano:
1.Python 3.10+
2.MongoDB Server (pokrenut lokalno na mongodb://localhost:27017)

Zatim je potrebno kreiranje i aktivacija virtualnog okruzenja venv:

Za Windows : python -m venv venv
venv\Scripts\activate
Aktivacija na Windows (PowerShell) — ukoliko dobijete grešku vezanu za izvršavanje skripti, pokrenuti:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1

Nakon toga instalirati zavisnosti: pip install -r requirements.txt

Aplikacija automatski kreira MongoDB time-series kolekciju events ukoliko ne postoji.
U slučaju da automatsko kreiranje ne uspe, potrebno je ručno kreirati kolekciju u MongoDB Compass-u.
Kreiranje Time-Series kolekcijeu MongoDB Compass-u:
1.Kreirati bazu: security_logs
2.Kreirati kolekciju: events
3.Označiti opciju Time-Series
Time Field: timestamp

Pokrenuti generisanje test podataka: python src/generate_logs.py
I na kraju pokrenuti aplikaciju : python src/app.py  ,aplikacija je dostupna na:
http://127.0.0.1:5000/
