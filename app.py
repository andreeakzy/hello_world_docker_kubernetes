
from flask import Flask, jsonify, request, Response, render_template_string  
import os
import socket
import time
import uuid
import threading
from datetime import datetime, timezone

app = Flask(__name__)

INSTANCE_ID = str(uuid.uuid4())
START_TS = time.time()
_hits = 0
_hits_lock = threading.Lock()

def inc_hits() -> int:
    # incrementeaza contorul thread safe
    global _hits
    with _hits_lock:
        _hits += 1
        return _hits

def uptime_seconds() -> int:
    # calculeaza uptime in sec
    return int(time.time() - START_TS)

def now_iso() -> str:
    # intoarce timpul curent utc in iso 8601
    return datetime.now(timezone.utc).isoformat()

APP_NAME = os.getenv("APP_NAME", "hello-flask-unique")
APP_GREETING = os.getenv("APP_GREETING", "salut din microserviciul meu unic")

@app.before_request
def _before():
    # numara fiecare request
    inc_hits()

@app.get("/")
def index():
    # endpoint principal json
    payload = {
        "message": APP_GREETING,
        "app_name": APP_NAME,
        "instance_id": INSTANCE_ID,
        "hostname": socket.gethostname(),
        "time_utc": now_iso(),
        "uptime_seconds": uptime_seconds(),
        "hits_total": _hits,
        "docs": {
            "health": "/healthz",
            "ready": "/readyz",
            "echo": "/echo",
            "time": "/time",
            "html": "/html"
        }
    }
    return jsonify(payload), 200

@app.get("/healthz")
def healthz():
    # liveness 
    return "ok", 200

@app.get("/readyz")
def readyz():
    if uptime_seconds() >= 2:
        return "ready", 200
    return Response("not ready", status=503)

@app.post("/echo")
def echo():
    # intoarce ce primeste (json sau text)
    if request.is_json:
        data = request.get_json(silent=True) or {}
        return jsonify({"you_sent": data, "time_utc": now_iso()}), 200
    txt = request.data.decode("utf-8") if request.data else ""
    return Response(f"you_sent: {txt}\n", mimetype="text/plain")

@app.get("/time")
def time_now():
    # timp server iso
    return jsonify({"time_utc": now_iso()}), 200

@app.get("/html")
def html():
    tpl = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>hello world</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
      :root { --bg:#0f172a; --fg:#e2e8f0; --muted:#94a3b8; --card:#111827; --acc:#38bdf8; }
      * { box-sizing: border-box; }
      body { margin:0; font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; background:linear-gradient(120deg,var(--bg),#1f2937); color:var(--fg); }
      .wrap { max-width: 860px; margin: 8vh auto; padding: 24px; }
      .card { background: var(--card); border-radius: 16px; padding: 24px; box-shadow: 0 10px 30px rgba(0,0,0,.35); }
      h1 { margin: 0 0 8px; font-size: clamp(28px,4vw,40px); }
      p { margin: 6px 0; color: var(--muted); }
      code { background: #0b1020; padding: 2px 6px; border-radius: 8px; }
      .badge { display:inline-block; padding:6px 10px; background: #0b1222; border:1px solid #1f2b46; border-radius:999px; margin-right:8px; }
      .accent { color: var(--acc); }
    </style>
  </head>
  <body>
    <div class="wrap">
      <div class="card">
        <h1><span class="accent">{{ app_name }}</span></h1>
        <p>{{ greeting }}</p>
        <p>instanta: <code>{{ instance }}</code></p>
        <p>hostname: <code>{{ host }}</code></p>
        <p>uptime: <code>{{ uptime }}s</code></p>
        <p>endpoints: <code>/healthz</code> · <code>/readyz</code> · <code>/echo</code> · <code>/time</code></p>
      </div>
    </div>
  </body>
</html>
    """
    return render_template_string(
        tpl,
        app_name=APP_NAME,
        greeting=APP_GREETING,
        instance=INSTANCE_ID,
        host=socket.gethostname(),
        uptime=uptime_seconds(),
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
