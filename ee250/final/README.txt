# Final_alenazrin

Team Members: Alena Novikova, Azrin Khan
GITHUB Repo: https://github.com/usc-ee250-fall2021/Final_alenazrin.git
Video DEMO: 

Instructions to execute code: 
1st terminal run: python3 weather_publisher.py
2nd terminal run: python3 laptop_the_subscriber.py
3rd terminal run: python3 rpi_pub_sub.py


List of external libraries used: 
import paho.mqtt.client as mqtt
import sys
import time
sys.path.append('../../Software/Python/') #importing GrovePi libraries to the system path
sys.path.append('../../Software/Python/grove_rgb_lcd') # This append is to support importing the LCD library.
import grovepi
from grovepi import dht
from grove_rgb_lcd import *
import threading
import requests

