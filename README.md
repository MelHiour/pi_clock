# pi_clock
Just clock and home weather station based on Raspberry Pi.

![device](../master/examples/animated.GIF)
![web_form](../master/examples/web_form_example.png)
![web_form_systyemd](../master/examples/web_form_example_systemd.png)
![pygal_graph](../master/examples/graph_example.png)

## Overview
A "solution" consists of several modules:
#### - piclock_poller.py
This is the core module which poles several plugged sensors (temperature, humidity, pressure) and grab data from Web (https://wttr.in/) for weather forecast. Script caches the data in memory using memcache. Runs via systemd service.
#### - piclock_display.py
This module works with simple 7-segment display. In a few words, it gets data from memcache and represent it for end-users (me and my family;). It also runs using systemd service.
#### - piclock_clear.py
Just clears display by sending four whitespaces (    ) to display. Executes via ExecStopPost= directive when piclock_display stops by systemd.
#### - piclock_db.py
Every hour data is serialized to sqlite database for further retrospective analisys. Script executes via crond.
The DB schema is very simple.

    CREATE TABLE weather (date text not NULL primary key,
                          inside_temp text,
                          humidity text,
                          pressure text,
                          outside_temp text,
                          co2 text,
                          tvoc text);

#### - piclock_web(_modules).py
Very simple web frontend (flask) for graphing (pygal). Basically, the SQL query is constructed based on user input. Data from database is used for building a graph. We have a quick link for today's graph as well as an ability to set custom timerange. Moreover, there is a hidden function to controll systemd services via web frontend by stating the service name and state in URL like http://pi.pc.hi/display.down or http://pi.pc.hi/poller.up.

That's it!

## Directory structure
```
.
├── piclock_clear.py                # Clears display    
├── piclock_db.py                   # Periodic serialization data to DB               
├── piclock_display.py              # Display data using 7-segment display
├── piclock_poller.py               # Sensors polling
├── piclock_web_modules.py          # Functions for gathering data from DB and graphing
├── piclock_web.py                  # Web Flask fronted
├── README.md                       # You are reading this
├── static                          # Static content
│   ├── apple-touch-icon.png            # favicon for apple
│   └── favicon.ico                     # favicon for "normal" devices...
├── systemd_services                # Here are some systemd service files stored
│   ├── piclock_display.service         # for display
│   ├── piclock_poller.service          # for poller
│   └── piclock_web.service             # for web frontend
├── temp-data.db                    # sqlite3 database
└── templates                       # Simple template for web page rendering
    └── index.html                      # index.html )
```

## Used
- [memcache](https://memcached.org)
- [pygal](http://www.pygal.org/en/stable/)
- [flask](http://flask.pocoo.org), [flask-caching](https://pypi.org/project/Flask-Caching)
- [Luma.LED_Matrix](https://github.com/rm-hull/luma.led_matrix): 7-segment display drivers for MAX7219
- [Adafruit_DHT](https://github.com/adafruit/Adafruit_Python_DHT): Drivers for AM2302 (temperature and humidity sensor)
- [Adafruit_BMP](https://github.com/adafruit/Adafruit-BMP085-Library): Drivers for BMP085 (barometric pressure and temperature)
- [Adafruit_CCS811](https://github.com/adafruit/Adafruit_CCS811): Drivers for CCS811 (air quality sensor (CO2, TVOC))
- [systemd-manager](https://github.com/emlid/systemd-manager)
- sqlite3, requests, re, etc...
