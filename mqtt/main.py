import time
import network
import utime
from umqtt.simple import MQTTClient
import dht
import machine
import json


# Default MQTT MQTT_BROKER to connect to
MQTT_BROKER = 'mqtt-dashboard.com'
MQTT_PORT = '1883'

CLIENT_ID = 'ESP32_Sensor'
TOPIC = b"norton/tcc/0560e0414c5086537ca878be8b4debbf/topic"

SSID = "Eureka_LSE"
SSID_PASSWORD = "HubEurekaLS3s2"
client = MQTTClient(CLIENT_ID, MQTT_BROKER, 1883, keepalive=60)

sensor = dht.DHT11(machine.Pin(18))


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


def dht_meansurement():
    sensor.measure()
    time.sleep(2)
    temp = sensor.temperature()
    hum = sensor.humidity()
    payload = dict(temperature=temp, humidity=hum)
    # print(f"Measurement", temp, hum)
    client.publish(TOPIC, json.dumps(payload))

# Received messages from subscriptions will be delivered to this callback
def sub_cb(topic, msg):
    if msg == b'{\n  "msg": "Server message"\n}':
        try:
            dht_meansurement()
            # read DHT22 here
        except OSError as e:
            print("Error ==>", e)
            client.publish(TOPIC, str("Cant read DHT11").encode())
    print(f"New message: {topic}, {msg}")


def main():
    client.connect()
    client.set_callback(sub_cb)
    client.subscribe('norton/tcc/topic')
    print(f"Connected to MQTT  Broker :: {MQTT_BROKER}, and waiting for callback function to be called!")

    while True:
        if True:
            # Blocking wait for message
            print(f'Connected to {MQTT_BROKER} MQTT broker, subscribed to {TOPIC} topic')
            client.check_msg()
            dht_meansurement()
            # client.publish(TOPIC, 'hello', retain=True)
            # client.wait_msg()
            time.sleep(5)
        else:
            # Non-blocking wait for message
            # client.check_msg()
            # Then need to sleep to avoid 100% CPU usage (in a real
            # app other useful actions would be performed instead)
            time.sleep(1)

    client.disconnect()


if __name__ == "__main__":
    main()
