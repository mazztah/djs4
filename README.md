# DJ NOTFALL-STUDIO (gross) 🎛

Das echte, grosse Studio - exakt deine beigefuegte Version:
`src/App.tsx` + `src/index.css` (React + Vite + Tailwind + Web Audio API)

## Was drin ist (aus deiner Datei)
- 4 Decks A B C D, Mixer, Fader, Crossfader, Filter, EQ
- Demo-Tracks: House 124, Techno 135, Hip-Hop 90, DnB 174, Disco 118, Chill 100
- Library mit 10 Eintraegen + 12 Stream-Tracks (SoundHelix, 1 Klick)
- Drum Machine (16 Steps), Synth (3 Oszillatoren), Piano, Sampler
- FX: Delay, Reverb, Flanger, Crush, Phaser, PingPong, Ducking
- Visualisierung, Master mit Limiter / Compressor / Loudness
- Fine-Tune Desks: Filter / Delay / Master mit Presets + Automation
- Hardware-Dropdown, Handy / Mic / Phone Panels
- Scenes / Sets / Presets, Dark / Light / Gold Themes, 65-Zoll Layout

## Schnellstart lokal (nur Frontend)
```bash
npm install
npm run dev
# -> http://localhost:5173
```

## Frontend gebaut + Backend zusammen lokal
```bash
npm run build
pip install -r requirements.txt
python app.py
# -> http://localhost:5000
```

## Deploy auf Render.com (Frontend + Backend zusammen)
Dieses Repo nutzt Docker, weil Frontend (Node) + Backend (Python) zusammen laufen.

1. Repo bei GitHub hochladen
2. Render -> New -> Web Service -> Repo waehlen
3. Render erkennt `render.yaml` automatisch (env: docker)
4. Start Command (steht im Dockerfile):
```
gunicorn -w 1 -b 0.0.0.0:$PORT app:app
```

## API (Backend)
- GET /api/health
- GET /api/tracks
- GET /api/stream-tracks
- GET /api/state, POST /api/state
- GET /api/presets, POST /api/presets
- GET /api/beats, POST /api/beats
- GET /api/random-mix

## Struktur
```
dj-notfall-studio-gross-repo/
  src/App.tsx        <- DEINE beigefuegte Datei, unveraendert
  src/index.css      <- DEINE beigefuegte Datei, unveraendert
  src/main.tsx
  index.html
  package.json
  vite.config.ts
  tsconfig.json
  tailwind.config.js
  postcss.config.js
  app.py             <- Python + Flask Backend
  requirements.txt
  Dockerfile
  render.yaml
  README.md
  LICENSE
  .gitignore
```

## Lizenz
MIT - siehe LICENSE

## NEU: Seite „Party + Chaos“ (Tab im Studio)
`public/party-chaos.html` vereint **dj-notfall-party-repo** (Party Mode) und **bass-chaos-v2** in einer Seite
mit *einem* Audio-Motor, *einem* BPM und *einem* Master. Im Studio als Tab **Party + Chaos** (oder Button „→ Party + Chaos“).
Die Seite übernimmt das Theme (Leder / Dark / Light) und läuft weiter, wenn man den Tab wechselt.

Enthalten: Party-Button, DJ-Battle, Chill, Tap-Tempo, Lucky Drop, Strobe/Vibration/Lampe, Crowd-Meter ·
2 Turntables + Crossfader · Track-Suche (Deezer, iTunes, Internet Archive, FMA) mit Favoriten ·
Drum Machine 16 Steps × 8 Spuren, 4 Beat-Slots · Melodie-Studio (8 Instrumente, Klavier, Speichern) · Synth + Akkorde ·
Voice-Recorder (Mikro) · Master-Aufnahme · 208 Sounds in 8 Boards · Pro-DJ-Top-10 · Presets.

### Zusätzliche API
- `GET /api/search?q=techno&sources=deezer,itunes,archive,fma`
- `GET /api/archive-file/<identifier>` · `GET /api/audio?url=…` (Audio-Proxy, nur Deezer/Apple/archive.org)
- `GET/POST /api/party/beats`, `DELETE /api/party/beats/<id>` (4 Slots, 8 Spuren × 16 Steps)
- `GET/POST /api/party/presets` · `GET /health`

### Lokal entwickeln
```bash
npm install
npm run dev            # Frontend :5173, /api wird an :5000 weitergereicht
python app.py          # Backend :5000 (zweites Terminal)
```
Hinweis: Deezer/iTunes liefern nur 30-Sekunden-Previews; Archive/FMA = CC/Public Domain, Lizenz je Track prüfen.
