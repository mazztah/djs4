# Stage 1: Frontend bauen (React + Vite)
FROM node:20 AS frontend
WORKDIR /app
# Alles kopieren - keine Einzeldatei mehr Pflicht, damit ein fehlendes
# vite.config.ts / tsconfig.json den Build nicht mehr abbricht
COPY . ./
# Falls package-lock.json fehlt, ist das ok - npm install legt es an
RUN npm install
RUN npm run build

# Stage 2: Python + Gunicorn, serviert dist/ + API
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py ./
COPY --from=frontend /app/dist ./dist
EXPOSE 5000
CMD ["sh", "-c", "gunicorn -w 1 --threads 8 --timeout 120 -b 0.0.0.0:$PORT app:app"]
