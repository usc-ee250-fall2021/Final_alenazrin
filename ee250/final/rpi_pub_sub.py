# Github Repo: https://github.com/usc-ee250-fall2021/Final_alenazrin.git
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
from grovepi import dht
from grove_rgb_lcd import *

import threading
lock = threading.Lock()

dht_sensor_port = 4 #temp sensor


RED_LED = 3
GREEN_LED = 7
BUZZER_PIN = 2

server_weather = 0
temp = 0

''' Buzzer stuff '''

length = 16;         #the number of notes 
tones = [ 2673, 2349, 2093, 2349, 2673, 0, 2673, 0, 2673, 2349, 2349, 0, 2349, 2673, 3136, 0 ] #mary had a little lamb lol
beats = [ 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1 ]
tempo = 400;

''' end '''

grovepi.pinMode(BUZZER_PIN, 1)

def play_song():
    for i in range (length):
         if tones[i] == 0:
            time.sleep(beats[i] * tempo / 1000)
         else:
            play_note(tones[i], beats[i] * tempo)
            
def play_note(tone, duration):
    for i in range (duration * 1000):
        grovepi.digitalWrite(BUZZER_PIN, 1)
        time.sleep(tone/1000000)
        grovepi.digitalWrite(BUZZER_PIN, 0)
        time.sleep(tone/1000000)
        i = i+tone*2
    
def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to the weather sensor topic here
    client.subscribe("alenazrin/weather_sensor")
    client.message_callback_add("alenazrin/weather_sensor", weather_sensor_callback)
    
    #subscribe to the weather from the server
    client.subscribe("alenazrin/weather_server")
    client.message_callback_add("alenazrin/weather_server", weather_server_callback)
    
    #subscribe to the led topic
    client.subscribe("alenazrin/led")
    client.message_callback_add("alenazrin/led", led_callback)
    
    

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
    
    temperature = float(str(message.payload, 'utf-8'))*(9/5) + 32
    global temp
    temp = str(temperature)
 
    print("Weather from the sensor: " + str(temp) + "F")
    difference = float(server_weather) - float(temp)
    #print("server weather value" + str(server_weather))
    if difference < 0:
        difference = difference*-1
    
    if difference > 5:
        with lock:
            grovepi.digitalWrite(RED_LED, 1) #light up the led
            grovepi.digitalWrite(GREEN_LED, 0)
        setRGB(255, 0, 0) #red lcd
        # ADD BUZZER?
        with lock:
            grovepi.digitalWrite(BUZZER_PIN, 1)
        time.sleep(2)
        with lock:
            grovepi.digitalWrite(BUZZER_PIN, 0)
    else:
        with lock:
            grovepi.digitalWrite(GREEN_LED, 1)
            grovepi.digitalWrite(RED_LED, 0)
        setRGB(0, 255, 0) #green lcd
        # ADD BUZZER?
        with lock:
            grovepi.digitalWrite(BUZZER_PIN, 0)
        
    #if float(temp) < 70:
        #play_song() # if cold, play Mary
        
    
#button callback
def weather_server_callback(client, userdata, message):
    print("Weather from the server: " + str(message.payload, 'utf-8') + "F")
    global server_weather
    server_weather = str(message.payload, 'utf-8') #set the var
    
'''  
# custom callback function for led callback
def led_callback(client, userdata, message):
    print(str(message.payload, 'utf-8'))
    if str(message.payload, 'utf-8') == "LED_ON":
        #print("got it")
        grovepi.digitalWrite(PORT1, 1)
        
    elif str(message.payload, 'utf-8') == "LED_OFF":
        #print("got it")
        grovepi.digitalWrite(PORT1, 0)
'''   
    
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
    setText(" ")

    while True:
        #print("delete this line")
        # read the temperature
        with lock:
            [ temperature, hum ] = dht(dht_sensor_port, 0)
        client.publish("alenazrin/weather_sensor", temperature)
      
        with lock:
            setText("Sensor: " + str(temp) + "F\nServer: " + str(server_weather) + "F")
        
        time.sleep(1)
