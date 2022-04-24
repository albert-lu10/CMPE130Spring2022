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

def partition(a, low, high):
    i = (low-1) 
    item=a[high]
    pivot = item["name"]
    for j in range(low, high):
        item2=a[j]
        
        if item2["name"] <= pivot:
            
            i = i+1
            a[i], a[j] = a[j], a[i]
    a[i+1], a[high] = a[high], a[i+1]
    return (i+1)
def quickSort(a, low, high):
    if len(a) == 1: 
        return a
    if low < high:
    
        p = partition(a, low, high)
        quickSort(a, low, p-1)
        quickSort(a, p+1, high)
    return (a)

@app.route('/sortbyprice', methods=['GET', 'POST'])

def sort_by_price():
    filename = os.path.join(app.static_folder, 'data', 'products.json')
    with open(filename) as file:
        data = json.load(file)
        
    sorted_data = quickSort(data,0,len(data)-1)
    return {'data': sorted_data}