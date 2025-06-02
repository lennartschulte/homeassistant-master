import paho.mqtt.client as mqtt
broker_address="43.154.166.244"  #mqtt address
port=1883  #mqtt port
topic = "PrintSuccess" #mqtt topic
username="test"
password="test"
client_id ="mqtt_printer"
qos = 2
def on_connect(client,userdate,flags,rc):
    #print("connected with result code"+str(rc))
    clinet.username_pw_set(username, password)
    client.subscribe(topic)

def on_message(client,userdata,message):
    print(f"Received Message:{message.payload.decode()}")
    received_message = message.payload.decode("utf-8")
    parts = received_message.split(";")
    if parts[0] == "3":
        print("printer get ticket")
    elif parts[0]=="4":
        print("printer printed success")
    elif parts[0] == "5":
        print("ticket over time,pls try again")
    else:
        print("don't know the stauts:")


clinet = mqtt.Client("printer_subscriber")
clinet.on_connect = on_connect
clinet.on_message = on_message
try:
    clinet.connect(broker_address,port,qos)
    clinet.loop_forever()
except KeyboardInterrupt:
    print("Disconnecting....")
    clinet.disconnect()
except Exception as e:
    print("An error occurred:",str(e))
    clinet.disconnect()