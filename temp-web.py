from flask import Flask, request, render_template
from temp_web_modules import db_to_graph

app = Flask(__name__)

@app.route('/')
def base_form():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def graphing():
    date_from = request.form['date_from']
    date_until = request.form['date_until']
    db_to_graph('/root/temp-data/temp-data.db', 'weather', '2019-02-02', '2019-02-03')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = True)
