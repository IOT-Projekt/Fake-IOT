import os
import logging
import paho.mqtt.client as mqtt
import json 
from datetime import datetime

# Configure logging for Docker (stdout)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Environment variables
BROKER_IP = os.getenv("BROKER_IP", "localhost")
PORT = int(os.getenv("BROKER_PORT", 1883))
TOPIC = os.getenv("TOPIC", "iot/devices/motion_sensor")
MQTT_USERNAME = os.getenv("MQTT_USERNAME", "your_username")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "your_password")
CLIENT_ID = os.getenv("CLIENT_ID", "motion-sensor")

# Initialize the MQTT client
client = mqtt.Client(client_id=CLIENT_ID)

# If username and password are set, use them for authentication
if MQTT_USERNAME and MQTT_PASSWORD:
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)


def on_connect(client, userdata, flags, rc):
    """Callback functions for MQTT client connection logging"""
    if rc == 0:
        logging.info("Connected to MQTT broker.")
        client.connected_flag = True
    else:
        logging.error(f"Connection failed with return code {rc}")
        client.connected_flag = False

def on_publish(client, userdata, mid):
    """Callback function for MQTT message publishing logging"""
    logging.info(f"Message {mid} published successfully.")

def shutdown(client):
    """Gracefully stops the MQTT client and disconnects."""
    logging.info("Shutting down...")
    
    # ensure the client exists before disconnecting
    if client:
        client.loop_stop()
        client.disconnect()
        logging.info("Disconnected from MQTT broker.")


# Set the callback functions
client.on_connect = on_connect
client.on_publish = on_publish

# connect to the broker
client.connect(BROKER_IP, PORT, keepalive=60)

def read_motion_input():
    """Reads fake motion data from the terminal."""
    
    # Simulate motion detection with terminal inputs
    motion_detected = input("Bewegung registriert? (y/n): ").lower().strip() == "y"
    time = input("Uhrzeit der Bewegung (hh:mm): ")
    
    # Convert time in hh:mm to timestamp: 1) combine with current date, 2) convert to Unix timestamp
    today = datetime.now().date()
    date_time = datetime.strptime(f"{today} {time}", "%Y-%m-%d %H:%M")
    
    timestamp = int(date_time.timestamp())
    
    return motion_detected, timestamp


def main():
    # Read fake motion data from terminal and publish it to the MQTT broker
    while True:
        motion_detected, timestamp = read_motion_input()

        # If no motion is detected, skip the rest of the loop
        if not motion_detected:
            logging.info("Keine Bewegung registriert.")
            continue
        
        # Create JSON payload with device_id
        payload = json.dumps({
            "source" : "mqtt",
            "device_id": CLIENT_ID,
            "motion_detected": motion_detected,
            "timestamp": timestamp
        })

        client.publish(TOPIC, payload)

if __name__ == "__main__":
    main()