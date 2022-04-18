from flask import render_template, flash, redirect, session, json
from application import app
import os

@app.route("/")
@app.route("/home")
def index():
    filename = os.path.join(app.static_folder, 'data', 'products.json')
    with open(filename) as file:
        data = json.load(file)
    return render_template("index.html", data=data)

def sort(x):
    #todo: Add sorting algorithms
    return x

@app.route('/sortbyprice', methods=['GET', 'POST'])
def sort_by_price():
    print("Sorting...")
    filename = os.path.join(app.static_folder, 'data', 'products.json')
    with open(filename) as file:
        data = json.load(file)
    sorted_data = sort(data)
    return {"data": sorted_data}