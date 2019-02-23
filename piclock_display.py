#!/usr/bin/python
import time
import memcache
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

shared = memcache.Client(['127.0.0.1:11211'], debug=0)

while True:
    now = datetime.now()
    if now.timetuple()[3] in range(10, 18):
        device.contrast(0x7F)
    else:
        seg.device.contrast(16)

    sensors_data = shared.get('sensors_data')
    if sensors_data:
        now = datetime.now()
        seg.text = '{:>4.1f}C{}'.format(sensors_data['inside_temp'], now.strftime("%H.%M"))
        time.sleep(2)

        now = datetime.now()
        seg.text = '{:>4.1f}H{}'.format(sensors_data['humidity'], now.strftime("%H.%M"))
        time.sleep(2)

        now = datetime.now()
        seg.text = '{:>3}P{}'.format(sensors_data['pressure'], now.strftime("%H.%M"))
        time.sleep(2)

        now = datetime.now()
        seg.text = '{:>3}T{}'.format(sensors_data['outside_temp'], now.strftime("%H.%M"))
        time.sleep(2)

    else:
        seg.text ='--------'
