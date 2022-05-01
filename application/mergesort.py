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

def merge(arr, l, m, r):
    item=arr[m]
    n1 = m - l + 1
    n2 = r - m
 
    L = [0] * (n1)
    R = [0] * (n2)
 
    for i in range(0, n1):
        item2=arr[j]
        L[i] = arr[l + i]
 
    for j in range(0, n2):
        R[j] = arr[m + 1 + j]
 
    i = 0     
    j = 0     
    k = l     
 
    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1
 
    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1

def mergeSortByName(arr, l, r):
    if l < r:
        m = l+(r-l)//2
        mergeSortByName(arr, l, m)
        mergeSortByName(arr, m+1, r)
        merge(arr, l, m, r)


def mergeSortByPrice(arr, l, r):
    if l < r:
        m = l+(r-l)//2
        mergeSortByPrice(arr, l, m)
        mergeSortByPrice(arr, m+1, r)
        merge(arr, l, m, r)

@app.route('/sortbyname', methods=['GET', 'POST'])

def sort_by_name():
    filename = os.path.join(app.static_folder, 'data', 'products.json')
    with open(filename) as file:
        data = json.load(file)
        
    sorted_data = mergeSortByName(data,0,len(data)-1)
    return {'data': sorted_data}

@app.route('/sortbyprice', methods=['GET', 'POST'])
def sort_by_price():
    filename = os.path.join(app.static_folder, 'data', 'products.json')
    with open(filename) as file:
        data = json.load(file)
        
    sorted_data = mergeSortByPrice(data,0,len(data)-1)
    return {'data': sorted_data}