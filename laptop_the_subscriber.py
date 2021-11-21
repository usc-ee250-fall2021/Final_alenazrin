"""EE 250L Final Project"""

# Github Repo: https://github.com/usc-ee250-fall2021/lab05-alenazrin/tree/lab05/ee250/lab05
# Team Memebers: Alena Novikova, Azrin Khan

import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to the ultrasonic weather sensor topic here
    client.subscribe("alenazrin/weather_sensor")
    client.message_callback_add("alenazrin/weather_sensor", weather_sensor_callback)
    
    #subscribe to the led topic
    client.subscribe("alenazrin/led")
    client.message_callback_add("alenazrin/led", led_callback)
    
    #subscribe to the led topic
    client.subscribe("alenazrin/buzzer")
    client.message_callback_add("alenazrin/buzzer", buzzer_callback)
    

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

#ranger callback
def led_callback(client, userdata, message):
    #the third argument is 'message' here unlike 'msg' in on_message 
    print("LED on!")
    
#button callback
def weather_sensor_callback(client, userdata, message):
    #the third argument is 'message' here unlike 'msg' in on_message 
    print("Weather sensor")
    
#buzzer callback
def buzzer_callback(client, userdata, message):
    #the third argument is 'message' here unlike 'msg' in on_message 
    print("Buzzer!")
    
if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:
        # print("delete this line")
        time.sleep(1)
