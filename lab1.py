print("Xin chào ThingsBoard")
from gc import collect
import paho.mqtt.client as mqttclient
import time
import json
import serial.tools.list_ports

BROKER_ADDRESS = "demo.thingsboard.io"
PORT = 1883
THINGS_BOARD_ACCESS_TOKEN = "sZ5B863s9OQWh3XEmoa8"

mess=""


bbc_port = "COM10"  # microbit's COM
if len(bbc_port) > 0:
    ser = serial.Serial(port=bbc_port, baudrate=115200)

def processData(data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    collect_data = {}   
    print(splitData)
    try:
        collect_data[splitData[1]]=splitData[2]
        client.publish('v1/devices/me/telemetry', json.dumps(collect_data), 1)
    except:
        pass
    #TODO: Add your source code to publish data to the server

def readSerial():
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(mess[start:end + 1])
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end+1:]


def subscribed(client, userdata, mid, granted_qos):
    print("Subscribed...")


# def recv_message(client, userdata, message):
#     print("Received: ", message.payload.decode("utf-8"))
#     temp_data = {'value': True}
#     try:
#         jsonobj = json.loads(message.payload)
#         if jsonobj['method'] == "setValue":
#             temp_data['value'] = jsonobj['params']
#             client.publish('v1/devices/me/attributes', json.dumps(temp_data), 1)
#     except:
#         pass

def recv_message(client, userdata, message):
    print("Received: ", message.payload.decode("utf-8"))
    temp_data = {'value':True}
    cmd = 0
    #TODO: Update the cmd to control 2 devices
    try:
        jsonobj = json.loads(message.payload)
        if jsonobj['method'] == "setLED":
            temp_data['value'] = jsonobj['params']
            client.publish('v1/devices/me/attributes', json.dumps(temp_data), 1)
            if jsonobj['params']==True: cmd = 1 
            else: cmd = 0
            # ser.write((jsonobj['method'] + ":" + str(jsonobj['params']) + "#\n").encode())
            # ser.write(str(jsonobj['params'] + "#\n").encode())
        if jsonobj['method'] == "setFAN":
            temp_data['value'] = jsonobj['params']
            client.publish('v1/devices/me/attributes', json.dumps(temp_data), 1)
            if jsonobj['params']==True: cmd = 2 
            else: cmd = 3
            # ser.write((jsonobj['method'] + ":" + str(jsonobj['params']) + "#\n").encode())
            # ser.write(str(jsonobj['params']) + "#\n").encode()
    except:
        pass

    if len(bbc_port) > 0:
        ser.write((str(cmd) + "#").encode())


def connected(client, usedata, flags, rc):
    if rc == 0:
        print("Thingsboard connected successfully!!")
        client.subscribe("v1/devices/me/rpc/request/+")
    else:
        print("Connection is failed")


client = mqttclient.Client("Gateway_Thingsboard")
client.username_pw_set(THINGS_BOARD_ACCESS_TOKEN)

client.on_connect = connected
client.connect(BROKER_ADDRESS, 1883)
client.loop_start()

client.on_subscribe = subscribed
client.on_message = recv_message

# temp = 20
# humi = 50
# light_intesity = 200
# counter = 0

# #lấy địa chỉ hiện tại thông qua địa chỉ IP
# my_location = geocoder.ip('me') 

# latitude= my_location.lat
# longitude = my_location.lng

while True:
    # collect_data = {'temperature': temp, 'humidity': humi, 'light':light_intesity,'latitude':latitude, 'longitude':longitude}
    # temp += 1
    # humi += 1
    # light_intesity += 50
    # client.publish('v1/devices/me/telemetry', json.dumps(collect_data), 1)
    if len(bbc_port) >  0:
        readSerial()

    time.sleep(10)