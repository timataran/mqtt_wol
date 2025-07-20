FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY run-mqtt-wol.py .

CMD ["python", "run-mqtt-wol.py"]
