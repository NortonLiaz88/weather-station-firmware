import time
import network
import utime
from umqtt.simple import MQTTClient
import random

# Default MQTT MQTT_BROKER to connect to
MQTT_BROKER = '192.168.0.132'
CLIENT_ID = 'ESP32_Sensor'
TOPIC = b"hello/topic"

SSID = "example"
SSID_PASSWORD = "example"
client = MQTTClient(CLIENT_ID, MQTT_BROKER, 1883, keepalive=60)


def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(SSID, SSID_PASSWORD)
        while not sta_if.isconnected():
            print("Attempting to connect....")
            utime.sleep(1)
    print('Connected! Network config:', sta_if.ifconfig())


print("Connecting to your wifi...")
do_connect()


# Received messages from subscriptions will be delivered to this callback
def sub_cb(topic, msg):
    if msg == b'{\n  "msg": "Server message"\n}':
        random_temp = random.randint(20, 50)
        client.publish(TOPIC, str(random_temp).encode())
        print(f"Publishing temperature :: {random_temp}")
    print(f"New message: {topic}, {msg}")


def main():
    client.connect()
    client.set_callback(sub_cb)
    client.subscribe('hello/topic')
    print(f"Connected to MQTT  Broker :: {MQTT_BROKER}, and waiting for callback function to be called!")

    while True:
        if True:
            # Blocking wait for message
            print(f'Connected to {MQTT_BROKER} MQTT broker, subscribed to {TOPIC} topic')
            client.check_msg()
            # client.publish(TOPIC, 'hello', retain=True)
            # client.wait_msg()
            time.sleep(1)
        else:
            # Non-blocking wait for message
            # client.check_msg()
            # Then need to sleep to avoid 100% CPU usage (in a real
            # app other useful actions would be performed instead)
            time.sleep(1)

    client.disconnect()


if __name__ == "__main__":
    main()
