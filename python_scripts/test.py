import json
import paho.mqtt.client as mqtt

broker_address = "192.168.178.78"
port = 1883
topic = "home/sensors"
username = "ha-mqtt"
password = "ha-mqtt"
client_id = "mqtt_publisher_py"

def connect_mqtt():
    client = mqtt.Client(client_id)
    client.username_pw_set(username, password)
    client.connect(broker_address, port)
    return client

if __name__ == "__main__":
    client = connect_mqtt()
    payload = {
        "sensor1": "value1",
        "sensor2": "value2"
    }
    client.publish(topic, json.dumps(payload))
    client.disconnect()
