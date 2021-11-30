"""EE 250L Final Project"""

# Github Repo: https://github.com/usc-ee250-fall2021/lab05-alenazrin/tree/lab05/ee250/lab05
# Team Memebers: Alena Novikova, Azrin Khan

import paho.mqtt.client as mqtt
import time
import sys
import time
# By appending the folder of all the GrovePi libraries to the system path here,
# we are successfully `import grovepi`
sys.path.append('../../Software/Python/')
# This append is to support importing the LCD library.
sys.path.append('../../Software/Python/grove_rgb_lcd')

import grovepi

from grove_rgb_lcd import *
import di_i2c

server_weather = 0

RED_LED = 1
GREEN_LED = 3
BUZZER_PIN = 2

''' Buzzer stuff '''

length = 16;         #the number of notes 
#tones[] = { 2673, 2349, 2093, 2349, 2673, 0, 2673, 0, 2673, 2349, 2349, 0, 2349, 2673, 3136, 0 }; #mary had a little lamb lol
#beats[] = { 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1 };
tempo = 400;

''' end '''

pinMode(BUZZER_PIN, output)

def play_song():
    for i in range (length):
         if tones[i] == 0:
            delay(beats[i] * tempo);
         else:
            play_note(tones[i], beats[i] * tempo)
            
def play_note(tone, duration):
    for i in range (duration * 1000):
        digitalWrite(BUZZER_PIN, HIGH);
        delayMicroseconds(tone);
        digitalWrite(BUZZER_PIN, LOW);
        delayMicroseconds(tone);
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
    print("Weather from the sensor: " + str(message.payload, 'utf-8') + "F")
    temp = str(message.payload, 'utf-8')
    setText_norefresh(temp) # output to the lcd screen
    difference = int(server_weather) - int(temp)
    if difference < 0:
        difference = difference*-1
    
    if difference > 3:
        grovepi.digitalWrite(RED_LED, 1) #light up the led
        setRGB(255, 0, 0) #red lcd
        # ADD BUZZER?
        digitalWrite(BUZZER_PIN, 1)
    else:
        grovepi.digitalWrite(GREEN_LED, 1)
        setRGB(0, 255, 0) #green lcd
        # ADD BUZZER?
        digitalWrite(BUZZER_PIN, 0)
        
    if temp < 70:
        play_song() # if cold, play Mary
        
    
#button callback
def weather_server_callback(client, userdata, message):
    print("Weather from the server: " + str(message.payload, 'utf-8') + "F")
    server_weather = str(message.payload, 'utf-8') #set the var
    
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
