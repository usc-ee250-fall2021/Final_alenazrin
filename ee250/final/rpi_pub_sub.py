"""EE 250L Lab 05 Starter Code
Run rpi_pub_and_sub.py on your Raspberry Pi."""
# Github Repo: https://github.com/usc-ee250-fall2021/lab05-alenazrin/tree/lab05/ee250/lab05
# Team Memebers: Alena Novikova, Azrin Khan
import paho.mqtt.client as mqtt
import sys
import time
# By appending the folder of all the GrovePi libraries to the system path here,
# we are successfully `import grovepi`
sys.path.append('../../Software/Python/')
# This append is to support importing the LCD library.
sys.path.append('../../Software/Python/grove_rgb_lcd')
import grovepi
from grove_rgb_lcd import *

PORT1 = 2 #led
PORT2 = 4 #ultrasonic ranger
PORT3 = 3 #button 
dht_sensor_port = 7 #temp sensor

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to the led topic here
    client.subscribe("alena/led")
    client.message_callback_add("alena/led", led_callback)

    #subscribe to the lcd topic here
    client.subscribe("alena/lcd")
    client.message_callback_add("alena/lcd", lcd_callback)
    
    
# custom callback function for led callback
def led_callback(client, userdata, message):
    print(str(message.payload, 'utf-8'))
    if str(message.payload, 'utf-8') == "LED_ON":
        #print("got it")
        grovepi.digitalWrite(PORT1, 1)
        
    elif str(message.payload, 'utf-8') == "LED_OFF":
        #print("got it")
        grovepi.digitalWrite(PORT1, 0)
        
    
        
# custom callback function for lcd callback
def lcd_callback(client, userdata, message):
    print(str(message.payload, 'utf-8'))
    if str(message.payload, 'utf-8') == "w":
        setText("w")
    elif str(message.payload, 'utf-8') == "a":
        setText("a")
    elif str(message.payload, 'utf-8') == "s":
        setText("s")     
    elif str(message.payload, 'utf-8') == "d":
        setText("d")     
    
#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:
        #print("delete this line")
        # read the ultrasonic value
        ultrasonic = grovepi.ultrasonicRead(PORT2)
        client.publish("alena/ultrasonicRanger", ultrasonic)
        # read the temperature
        [ temp, hum ] = dht(dht_sensor_port, 1)
        client.publish("alenazrin/weather_sensor", temp)
        #read button pressed/not pressed
        button = grovepi.digitalRead(PORT3)
        if button == 1:
            client.publish("alena/button", button)
        
        
        time.sleep(1)
