#!/usr/bin/python
import time
import json
import sqlite3
from datetime import datetime

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.virtual import viewport, sevensegment

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=1)
seg = sevensegment(device)

seg.text = 'LOVECECA'
for x in range(5):
    for intensity in range(16):
        seg.device.contrast(intensity * 16)
        time.sleep(0.1)

device.contrast(0x7F)
seg.device.contrast(16)

while True:
    with open('/tmp/piclock_sensors.json', 'r') as file:
        sensors_data = json.load(file)

    print(sensors_data)

    now = datetime.now()
    seg.text = '{:>4.1f}C{}'.format(sensors_data['temperature'], now.strftime("%H.%M"))
    time.sleep(2)

    now = datetime.now()
    seg.text = '{:>4.1f}H{}'.format(sensors_data['humidity'], now.strftime("%H.%M"))
    time.sleep(2)

    now = datetime.now()
    seg.text = '{:>3}P{}'.format(sensors_data['pressure'], now.strftime("%H.%M"))
    time.sleep(2)

    now = datetime.now()
    if sensors_data['outside_temp']:
        seg.text = '{:>3}T{}'.format(sensors_data['outside_temp'], now.strftime("%H.%M"))
        time.sleep(2)

    if datetime.timetuple(now)[4] != 0:
        logged = False
    else:
        if not logged:
            query = 'INSERT into weather values (?, ?, ?, ?, ?)'
            data = (str(now), str(sensors_data['temperature']), str(sensors_data['humidity']), str(sensors_data['pressure']), sensors_data['outside_temp'])
            with sqlite3.connect('/root/pi_clock/temp-data.db') as connector:
                connector.execute(query, data)
            logged = True
