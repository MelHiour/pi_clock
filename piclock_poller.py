#!/usr/bin/python
import time
import re
import requests
import memcache
import Adafruit_DHT
import Adafruit_BMP.BMP085 as BMP085

sensor = BMP085.BMP085()
shared = memcache.Client(['127.0.0.1:11211'], debug=0)

while True:
    humidity, inside_temp = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 17)
    pressure = sensor.read_pressure()*0.0075006157584566
    raw_weather = requests.get('http://wttr.in/?format=3')
    outside_temp = re.search(' ([-+]?\d{1,2})', raw_weather.text)

    sensors_data = {'inside_temp': inside_temp,
                    'humidity': humidity,
                    'pressure': int(pressure),
                    'outside_temp': outside_temp.group(1).lstrip('+')}

    shared.set('sensors_data', sensors_data)
    time.sleep(10)
