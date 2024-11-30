import time
import random
import paho.mqtt.client as mqtt

BROKER = "mosquitto"  # Broker hostname (use "localhost" if not using Docker)
PORT = 1883
TOPIC = "iot/devices/temperature"
CLIENT_ID = "fake-temp-device-001"

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

def main():
    # Create MQTT client
    client = mqtt.Client(CLIENT_ID)

    # Bind callbacks
    client.on_connect = on_connect
    client.on_publish = on_publish

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

    # Start publishing temperature readings
    try:
        while True:
            temperature = generate_temperature()
            payload = f'{{"temperature": {temperature}}}'
            result = client.publish(TOPIC, payload, qos=1)  # Use QoS 1 for acknowledgment
            status = result.rc
            if status == 0:
                print(f"Published: {payload} to topic: {TOPIC}")
            else:
                print(f"Failed to publish message to topic {TOPIC}, return code {status}")
            time.sleep(2)  # Delay between readings
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        client.loop_stop()  # Stop the network loop
        client.disconnect()
        
def on_log(client, userdata, level, buf):
    print(f"Log: {buf}")

client.on_log = on_log


if __name__ == "__main__":
    mqtt.Client.connected_flag = False
    main()
