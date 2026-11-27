"""
DJ NOTFALL-STUDIO (gross) - Backend inkl. Seite "Party + Bass Chaos"
Original Frontend: src/App.tsx + src/index.css (React + Vite + Tailwind)
Backend: Python + Flask

Lokal (Frontend dev):
  npm install
  npm run dev          -> http://localhost:5173
  python app.py        -> http://localhost:5000 (API + gebautes Frontend aus dist/)

Lokal (gebautes Frontend + Backend zusammen):
  npm run build
  python app.py        -> http://localhost:5000

Render (Docker, siehe Dockerfile + render.yaml):
  gunicorn -w 1 --threads 8 --timeout 120 -b 0.0.0.0:$PORT app:app
"""
import json, os, random, threading, urllib.parse, urllib.request
import requests
from flask import Flask, jsonify, request, send_from_directory, send_file, Response, abort
from flask_cors import CORS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(BASE_DIR, "dist")
DATA_FILE = os.path.join(BASE_DIR, "studio.json")

app = Flask(__name__, static_folder="dist", static_url_path="")
CORS(app)

TRACKS = [
    {"id": 0, "name": "House 124", "genre": "House", "bpm": 124, "key": "A-moll"},
    {"id": 1, "name": "Techno 135", "genre": "Techno", "bpm": 135, "key": "F-moll"},
    {"id": 2, "name": "Hip-Hop 90", "genre": "HipHop", "bpm": 90, "key": "C-moll"},
    {"id": 3, "name": "Drum & Bass 174", "genre": "DnB", "bpm": 174, "key": "G-moll"},
    {"id": 4, "name": "Disco 118", "genre": "Disco", "bpm": 118, "key": "D-Dur"},
    {"id": 5, "name": "Chill 100", "genre": "Chill", "bpm": 100, "key": "E-Dur"},
]

STREAM_TRACKS = [
    {"id": "stream-1", "name": "House Sunset", "genre": "House", "bpm": 124, "key": "A-moll", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"},
    {"id": "stream-2", "name": "Techno Pulse", "genre": "Techno", "bpm": 135, "key": "F-moll", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3"},
    {"id": "stream-3", "name": "Deep House Night", "genre": "House", "bpm": 122, "key": "C-Dur", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3"},
    {"id": "stream-4", "name": "Hip-Hop Boom", "genre": "HipHop", "bpm": 90, "key": "G-moll", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3"},
    {"id": "stream-5", "name": "DnB Rush", "genre": "DnB", "bpm": 174, "key": "D-moll", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3"},
    {"id": "stream-6", "name": "Disco Fever", "genre": "Disco", "bpm": 118, "key": "B-Dur", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-6.mp3"},
    {"id": "stream-7", "name": "Chill Vibes", "genre": "Chill", "bpm": 100, "key": "E-Dur", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-7.mp3"},
    {"id": "stream-8", "name": "Trap Night", "genre": "Trap", "bpm": 140, "key": "F-moll", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3"},
    {"id": "stream-9", "name": "Afro Heat", "genre": "Afro", "bpm": 112, "key": "A-moll", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-9.mp3"},
    {"id": "stream-10", "name": "Melodic Techno", "genre": "Techno", "bpm": 128, "key": "G-Dur", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-10.mp3"},
    {"id": "stream-11", "name": "LoFi Dreams", "genre": "LoFi", "bpm": 82, "key": "C-Dur", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-11.mp3"},
    {"id": "stream-12", "name": "Peak Time", "genre": "House", "bpm": 132, "key": "A-moll", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-12.mp3"},
]

DEFAULT_DATA = {"bpm": 128, "master": 0.8, "presets": [], "beats": [], "scenes": [], "hardware": "Kein Gerät",
                "party_beats": [], "party_presets": {}}
LOCK = threading.Lock()

def load_data():
    if not os.path.exists(DATA_FILE):
        save_data(DEFAULT_DATA)
        return dict(DEFAULT_DATA)
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            d = json.load(f)
        for k, v in DEFAULT_DATA.items():
            if k not in d:
                d[k] = v
        return d
    except Exception:
        return dict(DEFAULT_DATA)

def save_data(data):
    with LOCK:
        tmp = DATA_FILE + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp, DATA_FILE)

@app.route("/")
def index():
    dist_index = os.path.join(DIST_DIR, "index.html")
    if os.path.exists(dist_index):
        return send_file(dist_index)
    return send_file(os.path.join(BASE_DIR, "index.html"))

@app.route("/assets/<path:path>")
def assets(path):
    return send_from_directory(os.path.join(DIST_DIR, "assets"), path)

@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "app": "DJ NOTFALL-STUDIO (gross)", "version": "3.0.0"})

@app.route("/api/tracks", methods=["GET"])
def get_tracks():
    return jsonify(TRACKS)

@app.route("/api/stream-tracks", methods=["GET"])
def get_stream_tracks():
    return jsonify(STREAM_TRACKS)

@app.route("/api/state", methods=["GET"])
def get_state():
    return jsonify(load_data())

@app.route("/api/state", methods=["POST"])
def save_state():
    data = request.get_json(force=True)
    cur = load_data()
    cur.update(data)
    if "bpm" in cur:
        cur["bpm"] = int(max(20, min(180, int(cur["bpm"]))))
    save_data(cur)
    return jsonify({"ok": True, "state": cur})

@app.route("/api/presets", methods=["GET"])
def get_presets():
    return jsonify(load_data().get("presets", []))

@app.route("/api/presets", methods=["POST"])
def save_preset():
    data = request.get_json(force=True)
    cur = load_data()
    presets = cur.get("presets", [])
    preset = {"id": len(presets) + 1, "name": str(data.get("name", "Preset"))[:60], "bpm": int(data.get("bpm", 128))}
    presets.append(preset)
    cur["presets"] = presets
    save_data(cur)
    return jsonify({"ok": True, "preset": preset})

@app.route("/api/beats", methods=["GET"])
def get_beats():
    return jsonify(load_data().get("beats", []))

@app.route("/api/beats", methods=["POST"])
def save_beat():
    data = request.get_json(force=True)
    if not isinstance(data.get("steps"), list):
        return jsonify({"error": "steps muss eine Liste sein"}), 400
    cur = load_data()
    beats = cur.get("beats", [])
    beat = {"id": len(beats) + 1, "name": str(data.get("name", "Beat"))[:60], "bpm": int(max(20, min(180, int(data.get("bpm", 128))))), "steps": data["steps"]}
    beats.append(beat)
    cur["beats"] = beats
    save_data(cur)
    return jsonify({"ok": True, "beat": beat})

MIXES = [
    {"genre": "Keller-Techno", "bpm": 132, "line": "Der Bass kommt aus dem Keller - und bleibt da!"},
    {"genre": "Schlager-House", "bpm": 124, "line": "Alle singen mit, keiner weiss warum!"},
    {"genre": "Kuechen-Disco", "bpm": 118, "line": "Topf als Hi-Hat, Kochloeffel als Mikro!"},
    {"genre": "Balkon-Rave", "bpm": 140, "line": "Nachbarn tanzen heimlich mit. Ehrlich!"},
    {"genre": "Sofa-Bass", "bpm": 96, "line": "So weich, dass die Couch mitschaukelt."},
    {"genre": "Notfall-Polka", "bpm": 152, "line": "Achtung! Fuesse schneller als der Verstand!"},
    {"genre": "Feuerwehr-Funk", "bpm": 112, "line": "Loescht jeden schlechten Vibe in 3 Sekunden."},
    {"genre": "Garten-Party-Groove", "bpm": 122, "line": "Grill an, Bass an, Sorgen aus!"},
]

@app.route("/api/random-mix", methods=["GET"])
def random_mix():
    return jsonify(random.choice(MIXES))

# ======================================================================
#  PARTY + BASS CHAOS  (Seite /party-chaos.html)
#  zusammengefuehrt aus dj-notfall-party-repo + bass-chaos-v2
# ======================================================================
DRUM_TRACKS = ["Kick", "Snare", "Clap", "HiHat", "Open Hat", "808", "Tom", "Crash"]

@app.route("/health")
def health_plain():
    return jsonify({"status": "ok", "app": "DJ NOTFALL-STUDIO"})

@app.route("/api/party/beats", methods=["GET"])
def party_beats_get():
    return jsonify(load_data().get("party_beats", []))

@app.route("/api/party/beats", methods=["POST"])
def party_beats_save():
    data = request.get_json(force=True, silent=True) or {}
    pattern = data.get("pattern")
    if not isinstance(pattern, dict):
        return jsonify({"error": "pattern muss ein Objekt {Spur: [16 Werte]} sein"}), 400
    clean = {}
    for name in DRUM_TRACKS:
        row = pattern.get(name, [0] * 16)
        if not isinstance(row, list) or len(row) != 16:
            return jsonify({"error": f"Spur {name} braucht genau 16 Werte"}), 400
        clean[name] = [1 if x else 0 for x in row]
    slot = max(1, min(4, int(data.get("id", 1))))
    beat = {
        "id": slot,
        "name": str(data.get("name", f"Beat {slot}"))[:60],
        "bpm": int(max(20, min(200, int(data.get("bpm", 128))))),
        "swing": float(max(0, min(0.4, float(data.get("swing", 0))))),
        "genre": str(data.get("genre", "House"))[:30],
        "bass": str(data.get("bass", "fett"))[:30],
        "pattern": clean,
    }
    cur = load_data()
    beats = [b for b in cur.get("party_beats", []) if b.get("id") != slot] + [beat]
    cur["party_beats"] = sorted(beats, key=lambda b: b["id"])
    save_data(cur)
    return jsonify({"ok": True, "beat": beat})

@app.route("/api/party/beats/<int:beat_id>", methods=["DELETE"])
def party_beats_delete(beat_id):
    cur = load_data()
    cur["party_beats"] = [b for b in cur.get("party_beats", []) if b.get("id") != beat_id]
    save_data(cur)
    return jsonify({"ok": True})

@app.route("/api/party/presets", methods=["GET"])
def party_presets_get():
    return jsonify(load_data().get("party_presets", {}))

@app.route("/api/party/presets", methods=["POST"])
def party_presets_save():
    data = request.get_json(force=True, silent=True) or {}
    cur = load_data()
    preset = cur.get("party_presets", {})
    # nur einfache Werte (Zahl/Text) uebernehmen
    preset.update({str(k)[:30]: v for k, v in data.items() if isinstance(v, (int, float, str))})
    if "bpm" in preset:
        preset["bpm"] = int(max(20, min(200, int(preset["bpm"]))))
    cur["party_presets"] = preset
    save_data(cur)
    return jsonify({"ok": True, "presets": preset})

# ---------- Track-Suche (Deezer / iTunes / Internet Archive / FMA) ----------
def fetch_json(url, timeout=12):
    req = urllib.request.Request(url, headers={"User-Agent": "DJ-NOTFALL-STUDIO/3.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8", "ignore"))

@app.route("/api/search")
def api_search():
    """Aggregiert: ?q=techno&sources=deezer,itunes,archive,fma"""
    q = (request.args.get("q") or "techno").strip()[:120]
    sources = (request.args.get("sources") or "deezer,itunes,archive,fma").split(",")
    out, errors = [], {}
    if "deezer" in sources:
        try:
            d = fetch_json("https://api.deezer.com/search?q=" + urllib.parse.quote(q))
            for t in (d.get("data") or [])[:20]:
                out.append({"source": "DEEZER", "title": t.get("title"), "artist": (t.get("artist") or {}).get("name"),
                            "cover": (t.get("album") or {}).get("cover_medium"), "preview": t.get("preview"),
                            "duration": t.get("duration"), "bpm": None, "license": "30s Preview", "link": t.get("link")})
        except Exception as e:
            errors["deezer"] = str(e)
    if "itunes" in sources:
        try:
            d = fetch_json("https://itunes.apple.com/search?term=" + urllib.parse.quote(q) + "&media=music&limit=20")
            for t in (d.get("results") or []):
                out.append({"source": "ITUNES", "title": t.get("trackName"), "artist": t.get("artistName"),
                            "cover": (t.get("artworkUrl100") or "").replace("100x100bb", "600x600bb"), "preview": t.get("previewUrl"),
                            "duration": round((t.get("trackTimeMillis") or 0) / 1000), "bpm": None, "license": "30s Preview",
                            "link": t.get("trackViewUrl")})
        except Exception as e:
            errors["itunes"] = str(e)
    if "archive" in sources:
        try:
            aq = f"mediatype:audio AND licenseurl:*creativecommons* AND ({q})"
            url = ("https://archive.org/advancedsearch.php?q=" + urllib.parse.quote(aq) +
                   "&fl[]=identifier&fl[]=title&fl[]=creator&rows=20&page=1&output=json")
            d = fetch_json(url)
            for doc in ((d.get("response") or {}).get("docs") or []):
                ident = doc.get("identifier")
                cr = doc.get("creator")
                out.append({"source": "ARCHIVE", "title": doc.get("title"), "artist": ", ".join(cr) if isinstance(cr, list) else cr,
                            "cover": f"https://archive.org/services/img/{ident}", "preview": None, "duration": None, "bpm": None,
                            "license": "CC / Public Domain - Lizenz pruefen", "link": f"https://archive.org/details/{ident}",
                            "identifier": ident})
        except Exception as e:
            errors["archive"] = str(e)
    if "fma" in sources:
        out.append({"source": "FMA", "title": f"FMA-Suche: {q} (in neuem Tab oeffnen)", "artist": "Free Music Archive", "cover": "",
                    "preview": "", "duration": None, "bpm": None, "license": "CC - je Track pruefen",
                    "link": "https://freemusicarchive.org/search?query=" + urllib.parse.quote(q), "is_search_link": True})
    return jsonify({"query": q, "results": out, "errors": errors, "count": len(out)})

@app.route("/api/archive-file/<identifier>")
def archive_file(identifier):
    """Findet die echte MP3-Datei zu einem Archive-Item."""
    try:
        meta = fetch_json("https://archive.org/metadata/" + urllib.parse.quote(identifier, safe=""))
        mp3s = [f for f in (meta.get("files") or []) if (f.get("name") or "").lower().endswith(".mp3")]
        if not mp3s:
            return jsonify({"error": "kein mp3 gefunden"}), 404
        sized = sorted(mp3s, key=lambda x: int(x.get("size") or 0))
        ok = [f for f in sized if 0 < int(f.get("size") or 0) <= 25 * 1024 * 1024]
        name = (ok[-1] if ok else sized[0])["name"]
        return jsonify({"identifier": identifier, "file": name,
                        "url": f"https://archive.org/download/{urllib.parse.quote(identifier, safe='')}/{urllib.parse.quote(name)}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------- Audio-Proxy (gleiche Domain -> Web Audio darf Decks aufnehmen/visualisieren) ----------
ALLOWED_SUFFIXES = ("dzcdn.net", "deezer.com", "mzstatic.com", "apple.com", "archive.org")

def host_allowed(url):
    p = urllib.parse.urlparse(url)
    h = (p.hostname or "").lower()
    return p.scheme == "https" and any(h == s or h.endswith("." + s) for s in ALLOWED_SUFFIXES)

@app.route("/api/audio")
def audio_proxy():
    url = request.args.get("url", "")
    if not host_allowed(url):
        abort(400, "Host nicht erlaubt")
    headers = {"User-Agent": "DJ-NOTFALL-STUDIO/3.0"}
    if request.headers.get("Range"):
        headers["Range"] = request.headers["Range"]
    up = None
    for _ in range(4):  # Weiterleitungen einzeln pruefen, nie blind folgen
        up = requests.get(url, headers=headers, stream=True, timeout=15, allow_redirects=False)
        if up.status_code in (301, 302, 303, 307, 308):
            url = urllib.parse.urljoin(url, up.headers.get("Location", ""))
            up.close()
            if not host_allowed(url):
                abort(400, "Redirect nicht erlaubt")
            continue
        break
    if up is None or up.status_code not in (200, 206):
        abort(502)
    out = {"Accept-Ranges": "bytes", "Cache-Control": "public, max-age=86400"}
    for k in ("Content-Length", "Content-Range"):
        if up.headers.get(k):
            out[k] = up.headers[k]
    return Response(up.iter_content(64 * 1024), status=up.status_code,
                    content_type=up.headers.get("Content-Type", "audio/mpeg"), headers=out)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"DJ NOTFALL-STUDIO (gross) laeuft auf Port {port}")
    app.run(host="0.0.0.0", port=port, debug=False)
