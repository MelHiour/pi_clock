from flask import Flask, request, render_template
from temp_web_modules import db_to_graph

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def graphing():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        date_from = request.form['date_from']
        date_until = request.form['date_until']
    result = db_to_graph('/root/temp-data/temp-data.db', 'weather', '2019-02-02', '2019-02-03')
    print(result)
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = True)
