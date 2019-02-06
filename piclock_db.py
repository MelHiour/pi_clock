#!/usr/bin/python
import memcache
import sqlite3
from datetime import datetime

def data_to_db(db_path, table_name, sensors_data):
    now = datetime.now()
    query = 'INSERT into {} values (?, ?, ?, ?, ?)'.format(table_name)
    data = (str(now),
            str(sensors_data['inside_temp']),
            str(sensors_data['humidity']),
            str(sensors_data['pressure']),
            sensors_data['outside_temp'])
    with sqlite3.connect(db_path) as connector:
        connector.execute(query, data)

shared = memcache.Client(['127.0.0.1:11211'], debug=0)
sensors_data = shared.get('sensors_data')
data_to_db('/root/pi_clock/temp-data.db', 'weather', sensors_data)
