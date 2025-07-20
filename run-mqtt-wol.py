import os
import socket
import logging
from paho.mqtt.client import Client, CallbackAPIVersion

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


def send_wol(mac):
    try:
        mac_bytes = bytes.fromhex(mac.replace(":", "").replace("-", ""))
        magic = b'\xff' * 6 + mac_bytes * 16
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(magic, ("<broadcast>", 9))
        sock.close()
        logging.info(f"WOL packet sent to {mac}")
    except Exception as e:
        logging.error(f"Failed to send WOL to {mac}: {e}")


def on_message(client, userdata, msg):
    mac = msg.payload.decode().strip()
    if mac:
        send_wol(mac)


client = Client(CallbackAPIVersion.VERSION2)
host = os.environ.get("MQTT_HOST", "localhost")
port = int(os.environ.get("MQTT_PORT", "1883"))
topic = os.environ.get("MQTT_TOPIC", "wol/mac")
username = os.environ.get("MQTT_USERNAME")
password = os.environ.get("MQTT_PASSWORD")

if username and password:
    client.username_pw_set(username, password)

client.on_message = on_message
client.connect(host, port, 60)
client.subscribe(topic)

logging.info(f"Subscribed to MQTT {host}:{port}, topic '{topic}'")
client.loop_forever()
