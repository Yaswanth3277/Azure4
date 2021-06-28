import textwrap
from flask import Flask, render_template, request
import pyodbc
import redis
from pymongo import MongoClient
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import io
import base64
import numpy as np

app = Flask(__name__)

account_name = "advanceddatabasesystems"
account_key = "R1BmHYfoF6UU244ga8KFYOrID42/GS7FZb4FCKd2Pl5yzvnMYIRqhmCPj/JTwzkft6D5GsuFDVcY7bU7V3VIDQ=="
container_name = "assignment4"
connection_str = "DefaultEndpointsProtocol=https;AccountName=advanceddatabasesystems;AccountKey=R1BmHYfoF6UU244ga8KFYOrID42/GS7FZb4FCKd2Pl5yzvnMYIRqhmCPj/JTwzkft6D5GsuFDVcY7bU7V3VIDQ==;EndpointSuffix=core.windows.net"

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
    location = []
    cursor.execute("select distinct locationsource from graph_data")
    for data in cursor:
        for values in data:
            location.append(values)
    return render_template("index.html", location = location)


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

    cursor.execute("select * from graph_data where Mag>='-2.0' and Mag<='-1.0'")
    for data in cursor:
        earthquakes1.append(data)
    earthquake_len1 = len(earthquakes1)

    cursor.execute("select * from graph_data where Mag>='-1.0' and Mag<=0.0")
    for data in cursor:
        earthquakes2.append(data)
    earthquake_len2 = len(earthquakes2)

    cursor.execute("select * from graph_data where Mag>=0.0 and Mag<=1.0")
    for data in cursor:
        earthquakes3.append(data)
    earthquake_len3 = len(earthquakes3)

    cursor.execute("select * from graph_data where Mag>=1.0 and Mag<=2.0")
    for data in cursor:
        earthquakes4.append(data)
    earthquake_len4 = len(earthquakes4)

    cursor.execute("select * from graph_data where Mag>=2.0 and Mag<=3.0")
    for data in cursor:
        earthquakes5.append(data)
    earthquake_len5 = len(earthquakes5)

    cursor.execute("select * from graph_data where Mag>=3.0 and Mag<=4.0")
    for data in cursor:
        earthquakes6.append(data)
    earthquake_len6 = len(earthquakes6)

    cursor.execute("select * from graph_data where Mag>=4.0 and Mag<=5.0")
    for data in cursor:
        earthquakes7.append(data)
    earthquake_len7 = len(earthquakes7)

    cursor.execute("select * from graph_data where Mag>=5.0 and Mag<=6.0")
    for data in cursor:
        earthquakes8.append(data)
    earthquake_len8 = len(earthquakes8)

    cursor.execute("select * from graph_data where Mag>=6.0 and Mag<=7.0")
    for data in cursor:
        earthquakes9.append(data)
    earthquake_len9 = len(earthquakes9)

    cursor.execute("select * from graph_data where Mag>=7.0 and Mag<=8.0")
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
    plt.pie(pie_array, labels=labels, explode=explode, autopct='%.0f%%')
    figfile = io.BytesIO()
    plt.savefig(figfile, format='png')
    plt.close()
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    files = figdata_png.decode('utf-8')
    return render_template("mag_clusters.html", output = files)


@app.route('/earthquakeclustersmagtype', methods=['GET', 'POST'])
def earthquake_clusters_magtype():
    earthquakes1 = []
    earthquakes2 = []
    earthquakes3 = []
    earthquakes4 = []
    earthquakes5 = []
    earthquakes6 = []
    earthquakes7 = []
    earthquakes8 = []
    earthquakes9 = []
    types = []
    labels = []
    cursor.execute("select distinct Magtype from graph_data")
    for data in cursor:
        for value in data:
            if value != None:
                types.append(value)
    print(types)

    cursor.execute(
        "select * from graph_data where Magtype=?",
        types[0])
    for data in cursor:
        earthquakes1.append(data)
    earthquake_len1 = len(earthquakes1)

    cursor.execute(
        "select * from graph_data where Magtype=?",
        types[1])
    for data in cursor:
        earthquakes2.append(data)
    earthquake_len2 = len(earthquakes2)

    cursor.execute(
        "select * from graph_data where Magtype=?",
        types[2])
    for data in cursor:
        earthquakes3.append(data)
    earthquake_len3 = len(earthquakes3)

    cursor.execute(
        "select * from graph_data where Magtype=?",
        types[3])
    for data in cursor:
        earthquakes4.append(data)
    earthquake_len4 = len(earthquakes4)

    cursor.execute(
        "select * from graph_data where Magtype=?",
        types[4])
    for data in cursor:
        earthquakes5.append(data)
    earthquake_len5 = len(earthquakes5)

    cursor.execute(
        "select * from graph_data where Magtype=?",
        types[5])
    for data in cursor:
        earthquakes6.append(data)
    earthquake_len6 = len(earthquakes6)

    cursor.execute(
        "select * from graph_data where Magtype=?",
        types[6])
    for data in cursor:
        earthquakes7.append(data)
    earthquake_len7 = len(earthquakes7)

    cursor.execute(
        "select * from graph_data where Magtype=?",
        types[7])
    for data in cursor:
        earthquakes8.append(data)
    earthquake_len8 = len(earthquakes8)

    cursor.execute("Select Distinct Magtype from graph_data")
    for data in cursor:
        for value in data:
            if value != None:
                labels.append(value)

    print(labels)

    data_points = [earthquake_len1, earthquake_len2, earthquake_len3, earthquake_len4, earthquake_len5, earthquake_len6, earthquake_len7, earthquake_len8]
    print(data_points)

    plt.bar(labels, data_points)
    plt.xlabel("Earthquake Type")
    plt.ylabel("Count of earthquakes")
    plt.title("Earthquake count based on Type")
    figfile = io.BytesIO()
    plt.savefig(figfile, format='png')
    plt.close()
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    files = figdata_png.decode('utf-8')
    return render_template("magtype_clusters.html", outputs=files)


@app.route('/depthmag', methods=['GET', 'POST'])
def depth_mag():
    depth = []
    mag = []
    cursor.execute("select top 1000 depth from graph_data")
    for data in cursor:
        for value in data:
            depth.append(value)

    cursor.execute("select top 1000 mag from graph_data")
    for data in cursor:
        for value in data:
            mag.append(value)

    print(depth)
    print(mag)

    colors = cm.rainbow(np.linspace(0, 1, len(depth)))
    plt.scatter(depth, mag, c=colors)
    plt.xlabel("DEPTH")
    plt.ylabel("Magnitude")
    plt.title("Graph of Depth Vs Magnitude")
    figfile = io.BytesIO()
    plt.savefig(figfile, format='png')
    plt.close()
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    files = figdata_png.decode('utf-8')

    return render_template("depth_mag.html", dmoutputs = files)


@app.route("/locationsource", methods = ['GET', 'POST'])
def location_source():
    mags = []
    if request.method == 'POST':
        area = request.form.get('areas')

        cursor.execute("select mag from graph_data where locationsource = ?", area)
        for data in cursor:
            for value in data:
                mags.append(value)

    plt.hist(mags)
    plt.xlabel("Magnitude")
    plt.ylabel("Count")
    plt.title("Graph of Earthquakes based on LocationSource and Magnitude in")
    figfile = io.BytesIO()
    plt.savefig(figfile, format='png')
    plt.close()
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    files = figdata_png.decode('utf-8')

    return render_template('location_source.html', lsoutputs = files, area = area)


if __name__ == '__main__':
    app.run()
