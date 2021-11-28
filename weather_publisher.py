"""EE 250L Lab 05 Starter Code
Run vm_publisher.py in a separate terminal on your VM."""

# Github Repo: https://github.com/usc-ee250-fall2021/lab05-alenazrin/tree/lab05/ee250/lab05
# Team Memebers: Alena Novikova, Azrin Khan

import paho.mqtt.client as mqtt
import time
from pynput import keyboard

import requests

# OpenWeatherMap API: https://openweathermap.org/current

# Sign up for an API key
OWM_API_KEY = '7739ee4718f1d8cd3b44c2a8248ad2e3'  # OpenWeatherMap API Key

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
       

#Default message callback. Please use custom callbacks
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))
    
      
def get_weather():
    params = {
        'appid': OWM_API_KEY,
        # TODO: referencing the API documentation, add the missing parameters for zip code and units (Fahrenheit)
        'zip': 90089,  #zip code
        'units': 'imperial'  #unit Fahrenheit
    }
    
    response = requests.get('http://api.openweathermap.org/data/2.5/weather', params)

    if response.status_code == 200: # Status: OK
        data = response.json()

        #TODO: Extract the temperature & humidity from data, and return as a tuple
        temp = data["main"]["temp"]  #extract temp
        hum = data["main"]["humidity"]  #extract humidity
        return temp

    else:
        print('error: got response code %d' % response.status_code)
        print(response.text)
        return 0.0, 0.0

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:
        #print("delete this line")
        # get the temparature
        temp = get_weather()
        client.publish("alenazrin/server_weather", temp)
        time.sleep(1)
