#!/usr/bin/python
import time
import re
import requests
import memcache
import Adafruit_DHT
import Adafruit_BMP.BMP085 as BMP085
import Adafruit_CCS811.Adafruit_CCS811 as CCS811

sensor = BMP085.BMP085()
ccs =  CCS811()

shared = memcache.Client(['127.0.0.1:11211'], debug=0)
weather_regex = re.compile(' ([-+]?\d{1,2})')

while True:
    try:
        humidity, inside_temp = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 17)
        pressure = sensor.read_pressure()*0.0075006157584566
        raw_weather = requests.get('http://wttr.in/?format=3')
        outside_temp_raw = weather_regex.search(raw_weather.text)

        if ccs.available():
            if not ccs.readData():
                if len(str(ccs.geteCO2())) <= 4:
                    if len(str(ccs.getTVOC())) <= 4:
                        co2 = ccs.geteCO2()
                        tvoc = ccs.getTVOC()

    except requests.exceptions.ConnectionError:
        outside_temp_raw = False

    except IOError:
        pass

    finally:
        if outside_temp_raw:
            outside_temp = outside_temp_raw.group(1).lstrip('+')
        else:
            outside_temp = 'NA'

        sensors_data = {'inside_temp': inside_temp,
                        'humidity': humidity,
                        'pressure': int(pressure),
                        'outside_temp': outside_temp,
                        'co2': co2,
                        'tvoc': tvoc}

        shared.set('sensors_data', sensors_data, 300)
        time.sleep(30)
