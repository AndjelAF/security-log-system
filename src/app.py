from flask import Flask, jsonify, render_template
from mongo_analytics import (
    events_by_type,
    brute_force_by_user,
    brute_force_by_ip,
    attack_burst_detection,
    events_trend,
    suspicious_users
)

app = Flask(__name__, template_folder="templates")


# API rute
@app.route("/api/stats/types")
def api_types():
    return jsonify(events_by_type())


@app.route("/api/alerts/users")
def api_user_alerts():
    return jsonify(brute_force_by_user())


@app.route("/api/alerts/ip")
def api_ip_alerts():
    return jsonify(brute_force_by_ip())

@app.route("/api/alerts/burst")
def api_burst_alerts():
    return jsonify(attack_burst_detection())


@app.route("/api/stats/trend")
def api_trend():
    return jsonify(events_trend())
@app.route("/api/risk/users")
def api_risk_users():
    return jsonify(suspicious_users())


# Frontend ruta
@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)