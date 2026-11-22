FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app app
# Container needs 0.0.0.0 inside; compose publishes it on host loopback only.
ENV TUBESOMALI_HOST=0.0.0.0 TUBESOMALI_LAN_MODE=false
CMD ["python", "-m", "app"]
