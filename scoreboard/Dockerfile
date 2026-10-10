# payphone-phreak-lab :: scoreboard image
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY templates/ templates/
COPY static/ static/

RUN mkdir -p /data
ENV DB_PATH=/data/scoreboard.db
ENV PORT=8080
EXPOSE 8080

# Flask's dev server is fine for a meetup LAN. For anything bigger, put
# gunicorn in front (see docs/SETUP.md).
CMD ["python", "app.py"]
