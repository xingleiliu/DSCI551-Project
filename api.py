import flask
import matplotlib.pyplot as plt

plt.ioff()
import numpy as np

import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename

# import mpld3
# from mpld3 import plugins
# import json
# import random
# import scatterplots
# from datetime import date

UPLOAD_FOLDER = 'C:/Users/jenny/OneDrive/Desktop/USC/Fall 2021/DSCI 551/Project/uploads'
ALLOWED_EXTENSIONS = {'json', 'csv', 'txt', 'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploads/<name>')
def display_image(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    print(request.files)
    if "text-submit" in request.form:
        if request.method == 'POST':
            data = request.files['data']

            if data and allowed_file(data.filename):
                filename = secure_filename(data.filename)
                data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return redirect(url_for('display_image', name=filename))

    if "image-submit" in request.form:
        if request.method == 'POST':
            image = request.files['image']
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return render_template("index.html", filename=filename)
    return render_template("index.html")



# @app.route('/analysis/')
# def analysis():
#   today = date.today()
#   max_date = today.strftime("%Y-%m-%d")
#   min_date = "2020-04-01"
#   return render_template("analysis.html", min_date=min_date, max_date=max_date)
#
# @app.route('/research/')
# def research():
#   return render_template("research.html")
#
#
# # This function get the POST request and return the plot in format of html
# @app.route('/query', methods = ['POST'])
# def query():
#   # close all open figures to avoid memory leaks and server crashes
#   plt.close('all')
#
#   # Get data from ajax request
#   data = json.loads(request.data)
#   agent = request.headers.get('User-Agent')
#   print(agent)
#   mobile = False
#   if "mobile" in agent.lower():
#     mobile = True
#   return plot(data["country"], data["state"], data["start"], data["end"], mobile)


if __name__ == '__main__':
    app.run(debug=True)
