from flask import Flask, request, redirect
import datetime, json
import geoip2.database
import user_agents
import os
import requests

app = Flask(__name__)

# Шлях до GeoLite2 бази
MMDB_URL = os.getenv("MMDB_URL")
MMDB_PATH = "GeoLite2-City.mmdb"

if not os.path.exists(MMDB_PATH):
    print("GeoLite2-City.mmdb not found, downloading...")
    if not MMDB_URL:
        raise RuntimeError("MMDB_URL not set in environment variables")
    r = requests.get(MMDB_URL, timeout=120)
    r.raise_for_status()
    with open(MMDB_PATH, "wb") as f:
        f.write(r.content)
    print("Downloaded GeoLite2-City.mmdb, size:", os.path.getsize(MMDB_PATH))
    with open(MMDB_PATH, "rb") as f:
        head = f.read(10)
        print("First bytes:", head)
    assert os.path.getsize(MMDB_PATH) > 10_000_000, "GeoLite2-City.mmdb файл занадто малий!"

geoip_reader = geoip2.database.Reader(MMDB_PATH)

@app.route("/friend/<ref>")
def chess_friend(ref):
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

    if "Android" in ua.os.family:
        return redirect("https://play.google.com/store/apps/details?id=com.chess", code=302)

    elif "iOS" in ua.os.family or "iPhone" in ua.device.family or "iPad" in ua.device.family:
        return redirect("https://apps.apple.com/us/app/chess-play-learn/id329218549", code=302)

    else:
        return redirect(f"https://link.chess.com/friend/{ref}", code=302)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
