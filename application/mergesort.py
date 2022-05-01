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

def merge1(arr, l, m, r):
    item1=m-l+1
    n1=item1["name"]
    item2=r-m
    n2 = item2["name"]
 
    L = [0] * (n1)
    R = [0] * (n2)
 
    for i in range(0, n1):
        item3=L[i]
        item3["name"] = arr[l + i]
 
    for j in range(0, n2):
        item4=R[j]
        item4["name"] = arr[m + 1 + j]
 
    i = 0     
    j = 0     
    k = l     
 
    while i < n1 and j < n2:
        if item3["name"] <= item4["name"]:
            arr[k] = item3["name"]
            i += 1
        else:
            arr[k] = item4["name"]
            j += 1
        k += 1
 
    while i < n1:
        arr[k] = item3["name"]
        i += 1
        k += 1
    while j < n2:
        arr[k] = item4["name"]
        j += 1
        k += 1

def mergeSortbyName(arr, l, r):
    if l < r:
        m = l+(r-l)//2
        mergeSortbyName(arr, l, m)
        mergeSortbyName(arr, m+1, r)
        merge1(arr, l, m, r)

def merge2(arr, l, m, r):
    item1=m-l+1
    n1=item1["price"]
    item2=r-m
    n2 = item2["price"]
 
    L = [0] * (n1)
    R = [0] * (n2)
 
    for i in range(0, n1):
        item3=L[i]
        item3["price"] = arr[l + i]
 
    for j in range(0, n2):
        item4=R[j]
        item4["price"] = arr[m + 1 + j]
 
    i = 0     
    j = 0     
    k = l     
 
    while i < n1 and j < n2:
        if item3["price"] <= item4["price"]:
            arr[k] = item3["price"]
            i += 1
        else:
            arr[k] = item4["price"]
            j += 1
        k += 1
 
    while i < n1:
        arr[k] = item3["price"]
        i += 1
        k += 1
    while j < n2:
        arr[k] = item4["price"]
        j += 1
        k += 1

def mergeSortbyPrice(arr, l, r):
    if l < r:
        m = l+(r-l)//2
        mergeSortbyPrice(arr, l, m)
        mergeSortbyPrice(arr, m+1, r)
        merge2(arr, l, m, r)

@app.route('/sortbyname', methods=['GET', 'POST'])

def sort_by_name():
    filename = os.path.join(app.static_folder, 'data', 'products.json')
    with open(filename) as file:
        data = json.load(file)
        
    sorted_data = mergeSortbyName(data,0,len(data)-1)
    return {'data': sorted_data}

@app.route('/sortbyprice', methods=['GET', 'POST'])
def sort_by_price():
    filename = os.path.join(app.static_folder, 'data', 'products.json')
    with open(filename) as file:
        data = json.load(file)
        
    sorted_data = mergeSortbyPrice(data,0,len(data)-1)
    return {'data': sorted_data}