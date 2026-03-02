from flask import Flask, jsonify, render_template
from mongo_analytics import events_by_type, brute_force_by_user, brute_force_by_ip

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


# Frontend ruta
@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)