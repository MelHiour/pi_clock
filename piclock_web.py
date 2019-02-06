#!/usr/bin/python3
from datetime import datetime, timedelta
from flask import Flask, request, render_template
from piclock_web_modules import db_to_graph

app = Flask(__name__)
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
def graphing_today():
    now = datetime.now()
    date_from = now.strftime("%Y-%m-%d")
    date_until = (now + timedelta(days=1)).strftime("%Y-%m-%d")
    result = db_to_graph('/root/pi_clock/temp-data.db', 'weather', date_from, date_until)
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
