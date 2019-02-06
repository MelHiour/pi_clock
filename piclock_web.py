#!/usr/bin/python3
import os
from datetime import datetime, timedelta
from flask import Flask, request, render_template, send_from_directory
from flask_caching import Cache
from piclock_web_modules import db_to_graph

app = Flask(__name__)
app.config['CACHE_TYPE'] = 'simple'
app.cache = Cache(app)

@app.route('/', methods=['GET', 'POST'])
def graphing():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        date_from = request.form['date_from']
        date_until = request.form['date_until']
    result = db_to_graph('/root/pi_clock/temp-data.db', 'weather', date_from, date_until)
    return result

@app.route('/today')
@app.cache.cached(timeout=3600)
def graphing_today():
    now = datetime.now()
    date_from = now.strftime("%Y-%m-%d")
    date_until = (now + timedelta(days=1)).strftime("%Y-%m-%d")
    result = db_to_graph('/root/pi_clock/temp-data.db', 'weather', date_from, date_until)
    return result

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')

@app.route('/apple-touch-icon.png')
def favicon_iphone():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'apple-touch-icon.png')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
