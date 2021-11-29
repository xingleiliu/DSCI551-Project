import matplotlib.pyplot as plt

plt.ioff()
import numpy as np

import os
from flask import Flask, flash, request, redirect, url_for, send_file, render_template
from flask import send_from_directory
from werkzeug.utils import secure_filename
import pyrebase
import requests
import json
from PIL import Image
from PIL.ExifTags import TAGS
import numpy as np
import twitter
from geopy.geocoders import Nominatim
from GPSPhoto import gpsphoto

keyword1 = None
keyword2 = None

config = {
    "apiKey": "AIzaSyAgWOMHj5qSskp3T55lBhTCUQLxXsxKri4",
    "authDomain": "dsci-551-9dfe8.firebaseapp.com",
    "databaseURL": "https://dsci-551-9dfe8-default-rtdb.firebaseio.com",
    "projectId": "dsci-551-9dfe8",
    "storageBucket": "dsci-551-9dfe8.appspot.com",
    "messagingSenderId": "800340626987",
    "appId": "1:800340626987:web:7c58a51234cdf61a17246e",
    "measurementId": "G-7W2BM9T675",
    "serviceAccount": "serviceAccountKey.json"
}

firebase_storage = pyrebase.initialize_app(config)
storage = firebase_storage.storage()
firebase_url = "dsci-551-9dfe8.appspot.com/"
database_url = "https://dsci-551-9dfe8-default-rtdb.firebaseio.com/"
realtime_database_url = "https://proj-aa3d9-default-rtdb.firebaseio.com/"

UPLOAD_FOLDER = 'C:/Users/jenny/OneDrive/Desktop/USC/Fall 2021/DSCI 551/Project/uploads'
ALLOWED_EXTENSIONS = {'json', 'csv', 'txt', 'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# with open('uploads/firebase.json') as f:
#     jsondata = json.load(f)
# hey = requests.put(url=database_url + 'firebase.json', json=jsondata)
# print(hey)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# @app.route('/data')
# def display_data(name):
#     file_url = database_url + name
#     return

@app.route('/USC-Gold-Architecture.jpg')
def background():
    return send_file('USC-Gold-Architecture.jpg')


@app.route('/uploads/<name>')
def display_image(name):
    file_url = firebase_url + name
    # return send_file(file_url)
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


@app.route('/', methods=['Get', 'POST'])
def enter_keywords():
    if request.method == 'POST':
        f = request.form.get("first")
        keyword1 = f
        s = request.form.get("sec")
        keyword2 = s
        message = twitter.main(f, s)
        first = realtime_database_url + f + ".json"
        second = realtime_database_url + s + ".json"
        firstjson = requests.get(first).json()
        secondjson = requests.get(second).json()
        # first_score = np.mean([row['sentiment_scores'] for row in firstjson])
        # second_score = np.mean([row['sentiment_scores'] for row in firstjson])

        return render_template("index.html", firstjson=json.dumps(firstjson, indent=4), secondjson=json.dumps(secondjson), fkw=f, skw=s, message=message)
    # if "keyword-submit" in request.form:
    #     print("there is user input")

    return render_template("index.html")


@app.route('/json', methods=['GET', 'POST'])
def upload_file():
    if "text-submit" in request.form:
        if request.method == 'POST':
            data = request.files['data']

            if data and allowed_file(data.filename):
                print(data)
                filename = secure_filename(data.filename)
                path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                data.save(path)
                size = os.path.getsize(path)
                with open(path, encoding='utf8') as f:
                    jsondata = json.load(f)

                new_jsondata, message = twitter.userData(jsondata)
                requests.put(url=database_url + filename, json=jsondata)
                rows = len(jsondata)
                # return redirect(url_for('display_image', name=filename))
                # firstjson=json.dumps(jsondata),
                return render_template("json.html", firstjson=json.dumps(jsondata), secondjson=json.dumps(new_jsondata), message=message, rows=rows, size=size)
    return render_template("json.html")


@app.route('/image', methods=['GET', 'POST'])
def upload_image():
    if "image-submit" in request.form:
        if request.method == 'POST':
            image = request.files['image']
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(path)

                img = Image.open(path)


                exif = {TAGS[k]: v for k, v in img.getexif().items() if k in TAGS}

                # initialize Nominatim API
                geolocator = Nominatim(user_agent="geoapiExercises")

                gpsdata = gpsphoto.getGPSData(path)
                # Latitude & Longitude input
                Latitude = str(gpsdata['Latitude'])
                Longitude = str(gpsdata['Longitude'])

                location = geolocator.reverse(Latitude + "," + Longitude)

                address = location.raw['address']

                output = {}
                output["City"] = address.get('city', '')
                output["State"] = address.get('state', '')
                output["Country"] = address.get('country', '')
                output["Zip Code"] = address.get('postcode')
                output["DateTime"] = exif["DateTime"]
                output["Size (Height x Length)"] = (exif["ExifImageHeight"], exif["ImageLength"])

                storage.child(filename).put(path)
                return render_template("image.html", filename=filename, metadata=output)
    return render_template("image.html")


@app.route('/tagcloud1')
def cloud1():
    return send_file("wc11.png")


@app.route('/tagcloud2')
def cloud2():
    return send_file("wc22.png")


@app.route('/tagcloud11')
def cloud11():
    return send_file("wc1.png")


@app.route('/tagcloud22')
def cloud22():
    return send_file("wc2.png")


@app.route('/tagcloud3')
def cloud3():
    return send_file("wc3.png")


if __name__ == '__main__':
    app.run(debug=True)
