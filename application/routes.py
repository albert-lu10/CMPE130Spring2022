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

def partition1(a, low, high):
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

def quickSortbyName(a, low, high):
    if len(a) == 1: 
        return a
    if low < high:
    
        p = partition1(a, low, high)
        quickSortbyName(a, low, p-1)
        quickSortbyName(a, p+1, high)
    return (a)

def partition2(a, low, high):
    i = (low-1) 
    item=a[high]
    pivot = item["price"]
    for j in range(low, high):
        item2=a[j]
        
        if item2["price"] <= pivot:
            
            i = i+1
            a[i], a[j] = a[j], a[i]
    a[i+1], a[high] = a[high], a[i+1]
    return (i+1)

def quickSortbyPrice(a, low, high):
    if len(a) == 1: 
        return a
    if low < high:
    
        p = partition2(a, low, high)
        quickSortbyPrice(a, low, p-1)
        quickSortbyPrice(a, p+1, high)
    return (a)


@app.route('/sortbyname', methods=['GET', 'POST'])

def sort_by_name():
    filename = os.path.join(app.static_folder, 'data', 'products.json')
    with open(filename) as file:
        data = json.load(file)
        
    sorted_data = quickSortbyName(data,0,len(data)-1)
    return {'data': sorted_data}

@app.route('/sortbyprice', methods=['GET', 'POST'])
def sort_by_price():
    filename = os.path.join(app.static_folder, 'data', 'products.json')
    with open(filename) as file:
        data = json.load(file)
        
    sorted_data = quickSortbyPrice(data,0,len(data)-1)
    return {'data': sorted_data}