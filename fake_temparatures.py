import time
import random
import paho.mqtt.client as mqtt
import os

# Access the BROKER_IP environment variable
BROKER = os.getenv('BROKER_IP', 'localhost')  # Default to 'localhost' if the var is not set

# BROKER = "192.168.178.146"  # Use "localhost" if running the script outside Docker
PORT = 1883
TOPIC = "iot/devices/temperature"
CLIENT_ID = "fake-temp-device-" + str(random.randint(1, 1000))

# Access the MQTT username and password from environment variables
MQTT_USERNAME = os.getenv('MQTT_USERNAME', 'your_username')
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD', 'your_password')

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker!")
        client.connected_flag = True
    else:
        print(f"Failed to connect, return code {rc}")
        client.connected_flag = False

def on_publish(client, userdata, mid):
    print(f"Message {mid} published successfully!")

def generate_temperature():
    """Simulates temperature readings."""
    return round(random.uniform(-10, 40), 2)

def on_log(client, userdata, level, buf):
    print(f"Log: {buf}")

def main():
    # Create MQTT client
    client = mqtt.Client(CLIENT_ID)
    client.connected_flag = False  # Create flag in client

    # Set username and password
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

    # Bind callbacks
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_log = on_log

    # Connect to the broker
    try:
        client.connect(BROKER, PORT)
        client.loop_start()  # Start the network loop in the background
        while not client.connected_flag:
            print("Waiting for connection...")
            time.sleep(1)
    except Exception as e:
        print(f"Failed to connect to MQTT broker: {e}")
        return

    # Publish temperature readings
    try:
        while True:
            temperature = generate_temperature()
            result = client.publish(TOPIC, temperature)
            status = result[0]
            if status == 0:
                print(f"Sent `{temperature}` to topic `{TOPIC}`")
            else:
                print(f"Failed to send message to topic {TOPIC}")
            time.sleep(5)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()
