#!/usr/bin/python3
import os
import memcache
from datetime import datetime, timedelta
from flask import Flask, request, render_template, send_from_directory
from flask_caching import Cache
from piclock_web_modules import db_to_graph, service_control, service_stats

shared = memcache.Client(['127.0.0.1:11211'], debug=0)

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
cache.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def graphing():
    if request.method == 'GET':
        sensors_data = shared.get('sensors_data')
        return render_template('index.html',
                                inside_temp = sensors_data['inside_temp'],
                                humidity = sensors_data['humidity'],
                                pressure = sensors_data['pressure'],
                                outside_temp = sensors_data['outside_temp'],
                                co2 = sensors_data['co2'],
                                tvoc = sensors_data['tvoc'])
    else:
        date_from = request.form['date_from']
        date_until = request.form['date_until']
    result = db_to_graph('/root/pi_clock/temp-data.db',
                         'weather',
                         date_from,
                         date_until,
                         minor_labels = False,
                         air = request.form.get('air'))
    return result

@app.route('/today')
@cache.cached(timeout=3600)
def graphing_today():
    now = datetime.now()
    date_from = now.strftime("%Y-%m-%d")
    date_until = (now + timedelta(days=1)).strftime("%Y-%m-%d")
    result = db_to_graph('/root/pi_clock/temp-data.db',
                         'weather',
                         date_from,
                         date_until,
                         dots = False,
                         air = False)
    return result

@app.route('/<service>.<action>')
def systemd_control(service, action):
    return service_control('piclock_'+service, action)

@app.route('/stats')
def systemd_stats():
    return render_template('stats.html', stats = service_stats())

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')

@app.route('/apple-touch-icon.png')
def favicon_iphone():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'apple-touch-icon.png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
