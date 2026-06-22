# ── Base image ──────────────────────────────────────────────
FROM python:3.11-slim

# ── Set working directory inside the container ──────────────
WORKDIR /app

# ── Copy dependencies list FIRST (cache trick) ──────────────
COPY requirements.txt .

# ── Install dependencies ─────────────────────────────────────
RUN pip install --no-cache-dir -r requirements.txt

# ── Copy the rest of the app code ───────────────────────────
COPY . .

# ── Tell Docker which port the app listens on ───────────────
EXPOSE 5000

# ── Start the app with gunicorn (production server) ─────────
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]