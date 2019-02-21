import pygal
import sqlite3
from pygal.style import DarkSolarizedStyle
from sysdmanager import SystemdManager

def get_db_data(db_path, table_name, from_date, until_date):
    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()
        cursor.execute("select * from {} where date between '{}' and '{}'".format(table_name, from_date, until_date))
        result = cursor.fetchall()
    return result

def graph_from_data(data, dots, minor_labels):
    time = []
    inside_temp = []
    humidity = []
    pressure = []
    outside_temp = []

    for item in data:
        time.append(item[0].split('.')[0])
        inside_temp.append(float(item[1]))
        humidity.append(float(item[2]))
        pressure.append(float(item[3])-700)
        if item[4] == 'NA':
            outside_temp.append(None)
        else:
            outside_temp.append(float(item[4]))

    line_chart = pygal.Line(x_label_rotation=-45,
                            interpolate='hermite',
                            allow_interruptions = True,
                            x_labels_major_every=10,
                            show_minor_x_labels = minor_labels,
                            show_only_major_dots = dots,
                            style=DarkSolarizedStyle)

    line_chart.title = "Weather conditions"
    
    line_chart.x_labels = time
    line_chart.add('inside_temp', inside_temp)
    line_chart.add('humidity', humidity)
    line_chart.add('pressure+700', pressure)
    line_chart.add('outside_temp', outside_temp)
   
    return line_chart.render_response()

def db_to_graph(db_path, table_name, from_date, until_date, dots = True, minor_labels = True):
    return graph_from_data(get_db_data(db_path, table_name, from_date, until_date), dots, minor_labels)

def service_control(service, action):
    manager = SystemdManager()
    if action == up:
        manager.start_unit("{}.service".format(service))
        return "{}.service has been started".format(service))
    elif action == down:
        manager.stop_unit("{}.service".format(service))
        return "{}.service has been stopped".format(service))
    else:
        return 'Only up/down are supported'
    
def main():
    db_to_graph('/root/temp-data/temp-data.db', 'weather', '2019-02-02', '2019-02-03')

if __name__ == '__main__':
    main()
