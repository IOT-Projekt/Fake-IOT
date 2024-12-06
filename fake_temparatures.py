import os
import time
import random
import math
import signal
import logging
import paho.mqtt.client as mqtt
import json 

# Configure logging for Docker (stdout)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Constants and defaults
DEFAULT_BROKER = "localhost"
DEFAULT_PORT = 1883
DEFAULT_TOPIC = "TOPIC NOT FOUND"
CLIENT_ID_PREFIX = "fake-temp-device-"

# Environment variables
BROKER = os.getenv("BROKER_IP", DEFAULT_BROKER)
PORT = int(os.getenv("BROKER_PORT", DEFAULT_PORT))
TOPIC = os.getenv("TOPIC", DEFAULT_TOPIC)
MQTT_USERNAME = os.getenv("MQTT_USERNAME", "your_username")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "your_password")

# Global flag for controlling the main loop
RUNNING = True

def simulate_temperature(base_temp=20.0, amplitude=10.0, noise=0.5, time_step=0.1):
    """
    Simulates realistic temperature readings:
    - `base_temp`: The average temperature.
    - `amplitude`: The maximum deviation due to day-night cycles.
    - `noise`: Random noise added to the temperature.
    - `time_step`: Time progression for the diurnal cycle (affects how fast the pattern evolves).
    """
    time_of_day = time.time() % (24 * 3600)  # Simulate 24-hour cycle
    day_fraction = time_of_day / (24 * 3600)  # Fraction of the day (0.0 to 1.0)
    temperature = base_temp + amplitude * math.sin(2 * math.pi * day_fraction)
    temperature += random.uniform(-noise, noise)  # Add random noise
    return round(temperature, 2)

def on_connect(client, userdata, flags, rc):
    """
    Callback triggered when the client connects to the broker.
    """
    if rc == 0:
        logging.info("Connected to MQTT broker.")
        client.connected_flag = True
    else:
        logging.error(f"Connection failed with return code {rc}")
        client.connected_flag = False

def on_publish(client, userdata, mid):
    """
    Callback triggered when a message is published.
    """
    logging.info(f"Message {mid} published successfully.")

def shutdown(client):
    """
    Gracefully stops the MQTT client and disconnects.
    """
    global RUNNING
    RUNNING = False
    logging.info("Shutting down...")
    if client:
        client.loop_stop()
        client.disconnect()
        logging.info("Disconnected from MQTT broker.")

def handle_signals(signal_num, frame):
    """
    Handles termination signals for Docker.
    """
    logging.info(f"Received termination signal: {signal_num}")
    shutdown(client=None)

def configure_mqtt_client(client_id):
    """
    Configures the MQTT client with callbacks and credentials.
    """
    client = mqtt.Client(client_id)
    client.connected_flag = False

    # Set username and password for authentication
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

    # Bind callbacks
    client.on_connect = on_connect
    client.on_publish = on_publish

    return client

def main():
    """
    Main entry point for the script.
    """
    global RUNNING
    client_id = f"{CLIENT_ID_PREFIX}{random.randint(1, 1000)}"
    client = configure_mqtt_client(client_id)

    # Register signal handlers for Docker
    signal.signal(signal.SIGTERM, handle_signals)
    signal.signal(signal.SIGINT, handle_signals)

    # Connect to the broker
    try:
        logging.info("Connecting to broker...")
        client.connect(BROKER, PORT)
        client.loop_start()
        while not client.connected_flag:
            logging.info("Waiting for connection...")
            time.sleep(1)
    except Exception as e:
        logging.error(f"Failed to connect to MQTT broker: {e}")
        return

    # Publish temperature readings
    try:
        while RUNNING:
            temperature = simulate_temperature()
            timestamp = int(time.time())  # Current Unix timestamp (seconds)

            # Create JSON payload with device_id
            payload = json.dumps({
                "device_id": client_id,
                "temperature": temperature,
                "timestamp": timestamp
            })

            result = client.publish(TOPIC, payload)
            if result[0] == 0:
                logging.info(f"Sent `{payload}` to topic `{TOPIC}`")
            else:
                logging.error(f"Failed to send message to topic `{TOPIC}`")
            time.sleep(5)  # Adjust interval as needed
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    finally:
        shutdown(client)

if __name__ == "__main__":
    main()