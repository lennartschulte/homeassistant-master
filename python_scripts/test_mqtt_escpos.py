# 实例化 ESCPOSManager 对象
import random
import string
import ESCPOS_COMMAND
import paho.mqtt.client as mqtt
broker_address="192.168.178.78"  #mqtt address
port=1883  #mqtt port
topic = "Prn062523002F0C0A29000013241289A8B9" #mqtt topic
username="ha-mqtt"
password="ha-mqtt"
client_id ="mqtt_printer_py"
qos = 2

# connected the MQTT SERVER
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc==0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect to MQTT,Return code %d\n ",rc)
    client = mqtt.Client(client_id)
    client.on_connect = on_connect
    client.username_pw_set(username,password)
    client.connect(broker_address,port,qos)
    return client

#publsh the manager to printer
if __name__ == "__main__":
    client = connect_mqtt()
    esc_comm = ESCPOS_COMMAND.ESCPOSManager()
    esc_comm.Prefix_command()  #
    esc_comm.set_alignment("center")
    esc_comm.print_text("TEST IT FROM MQTT\n")
    esc_comm.set_font_size(128)
    esc_comm.print_text("this is big test\n")
    esc_comm.feed_lines(1)
    esc_comm.set_font_size(9)
    esc_comm.print_text("welcome to hspos test from MQTT,If you like our test please,click on the links \n")
    esc_comm.feed_lines(1)
    esc_comm.print_qr_code("www.hsprinter.com\n")
    esc_data = esc_comm.send_command()
    client.publish(topic, esc_data)
    client.disconnect()