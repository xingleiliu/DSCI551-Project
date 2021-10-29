import flask
import matplotlib.pyplot as plt
plt.ioff()
import numpy as np
from flask import send_file, render_template, request, json
# import os
# import mpld3
# from mpld3 import plugins
# import json
# import random
# import scatterplots
# from datetime import date

app = flask.Flask(__name__)

@app.route('/')
def home():
  # return "hello world"
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
# @app.route('/members/')
# def members():
#   return render_template("members.html")
#
# @app.route('/timeline/')
# def timeline():
#   return render_template("timeline.html")
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

