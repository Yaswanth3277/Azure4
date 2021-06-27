import textwrap
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import pandas as pd
import pyodbc
import timeit
import redis
import hashlib
import pickle
from pymongo import MongoClient
import numpy as np
import matplotlib.pyplot as plt
import mpld3

app = Flask(__name__)

driver = '{ODBC Driver 17 for SQL Server}'
server_name = 'anonymous'
database_name = 'csvdatabase'
username = "anonymous"
password = "Yash@3277"
server = '{server_name}.database.windows.net,1433'.format(server_name=server_name)
connection_string = textwrap.dedent('''
    Driver={driver};
    Server={server};
    Database={database};
    Uid={username};
    Pwd={password};
    Encrypt=yes;
    TrustServerCertificate=no;
    Connection Timeout=30;
'''.format(
    driver=driver,
    server=server,
    database=database_name,
    username=username,
    password=password
))
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()
r = redis.StrictRedis(host='adb3.redis.cache.windows.net',port=6380, db=0, password='qPurtLYjO4JUn0r0jvbjmifZd5+PA7KkBiOyKD8QK10=', ssl=True)
result = r.ping()
print("Ping returned : " + str(result))

mconnection_string = "mongodb://adb3:hSancCqD5F8mYEkorkOAEtoFVqY8p9sOj6kUoUOFkVRgCDnGxfQuJ9SPnQH8xEsKW7Rn5avZn6A5X5C3PBc7VQ==@adb3.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@adb3@"

client = MongoClient(r"mongodb://adb3:hSancCqD5F8mYEkorkOAEtoFVqY8p9sOj6kUoUOFkVRgCDnGxfQuJ9SPnQH8xEsKW7Rn5avZn6A5X5C3PBc7VQ==@adb3.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@adb3@")
db = client.adb3
todos = db.quakedata_3


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")


@app.route('/earthquakeclusters', methods=['GET', 'POST'])
def earthquake_clusters():
    earthquakes1 = []
    earthquakes2 = []
    earthquakes3 = []
    earthquakes4 = []
    earthquakes5 = []
    earthquakes6 = []
    earthquakes7 = []
    earthquakes8 = []
    earthquakes9 = []
    earthquakes10 = []
    pie_array = []

    cursor.execute("select Time, Latitude, Longitude, Depth, Mag, Magtype, Place, LocationSource from graph_data where Mag>='-2.0' and Mag<='-1.0'")
    for data in cursor:
        earthquakes1.append(data)
    earthquake_len1 = len(earthquakes1)

    cursor.execute("select Time, Latitude, Longitude, Depth, Mag, Magtype, Place, LocationSource from graph_data where Mag>='-1.0' and Mag<=0.0")
    for data in cursor:
        earthquakes2.append(data)
    earthquake_len2 = len(earthquakes2)

    cursor.execute("select Time, Latitude, Longitude, Depth, Mag, Magtype, Place, LocationSource from graph_data where Mag>=0.0 and Mag<=1.0")
    for data in cursor:
        earthquakes3.append(data)
    earthquake_len3 = len(earthquakes3)

    cursor.execute("select Time, Latitude, Longitude, Depth, Mag, Magtype, Place, LocationSource from graph_data where Mag>=1.0 and Mag<=2.0")
    for data in cursor:
        earthquakes4.append(data)
    earthquake_len4 = len(earthquakes4)

    cursor.execute("select Time, Latitude, Longitude, Depth, Mag, Magtype, Place, LocationSource from graph_data where Mag>=2.0 and Mag<=3.0")
    for data in cursor:
        earthquakes5.append(data)
    earthquake_len5 = len(earthquakes5)

    cursor.execute("select Time, Latitude, Longitude, Depth, Mag, Magtype, Place, LocationSource from graph_data where Mag>=3.0 and Mag<=4.0")
    for data in cursor:
        earthquakes6.append(data)
    earthquake_len6 = len(earthquakes6)

    cursor.execute("select Time, Latitude, Longitude, Depth, Mag, Magtype, Place, LocationSource from graph_data where Mag>=4.0 and Mag<=5.0")
    for data in cursor:
        earthquakes7.append(data)
    earthquake_len7 = len(earthquakes7)

    cursor.execute("select Time, Latitude, Longitude, Depth, Mag, Magtype, Place, LocationSource from graph_data where Mag>=5.0 and Mag<=6.0")
    for data in cursor:
        earthquakes8.append(data)
    earthquake_len8 = len(earthquakes8)

    cursor.execute("select Time, Latitude, Longitude, Depth, Mag, Magtype, Place, LocationSource from graph_data where Mag>=6.0 and Mag<=7.0")
    for data in cursor:
        earthquakes9.append(data)
    earthquake_len9 = len(earthquakes9)

    cursor.execute("select Time, Latitude, Longitude, Depth, Mag, Magtype, Place, LocationSource from graph_data where Mag>=7.0 and Mag<=8.0")
    for data in cursor:
        earthquakes10.append(data)
    earthquake_len10 = len(earthquakes10)

    cursor.execute("select count(*) from graph_data")
    for data in cursor:
        for value in data:
            earthquake_total = value
    print(earthquake_total)

    pie_array.append((earthquake_len1/earthquake_total)*100)
    pie_array.append((earthquake_len2/earthquake_total)*100)
    pie_array.append((earthquake_len3/earthquake_total)*100)
    pie_array.append((earthquake_len4/earthquake_total)*100)
    pie_array.append((earthquake_len5/earthquake_total)*100)
    pie_array.append((earthquake_len6/earthquake_total)*100)
    pie_array.append((earthquake_len7/earthquake_total)*100)

    print(pie_array)

    labels = ["Mag(-2to-1)","Mag(-1to0)","Mag(0to1)","Mag(1to2)","Mag(2to3)","Mag(3to4)","Mag(4to5)"]
    explode = [0.2,0.2,0.2,0.2,0.2,0.2,0.2]
    fig = plt.pie(pie_array, labels=labels, explode=explode, autopct='%.0f%%')
    plt.savefig('static/clusters_plot.jpg')
    plt.show()

    return render_template('mag_clusters.html', earthquakes1 = earthquakes1, length1= earthquake_len1, earthquakes2 = earthquakes2, length2= earthquake_len2, earthquakes3 = earthquakes3, length3= earthquake_len3, earthquakes4 = earthquakes4, length4= earthquake_len4, earthquakes5 = earthquakes5, length5= earthquake_len5, earthquakes6 = earthquakes6, length6= earthquake_len6, earthquakes7 = earthquakes7, length7= earthquake_len7, earthquakes8 = earthquakes8, length8= earthquake_len8, earthquakes9 = earthquakes9, length9= earthquake_len9, earthquakes10 = earthquakes10, length10= earthquake_len10)

if __name__ == '__main__':
    app.run()