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


def partition(data, low, high):
    i = (low-1) 
    item=data[high]
    pivot = item["name"] 
    
    for j in range(low, high):
        item2=data[j]
        
        if item2["name"] <= pivot:
            
            i = i+1
            data[i], data[j] = data[j], data[i]
            
    data[i+1], data[high] = data[high], data[i+1]
    return (i+1)

def quickSortbyName(data, low, high):
    if len(data) == 1: 
        return data
    if low < high:
        
        p = partition(data, low, high)
        quickSortbyName(data, low, p-1)
        quickSortbyName(data, p+1, high)





@app.route('/sortbyprice', methods=['GET', 'POST'])
def quickSortbyName():
    
    print("Sorting...")
    filename = os.path.join(app.static_folder, 'data', 'products.json')
    with open(filename) as file:
        data = json.load(file)
    
    sorted_data = quickSortbyName(data,0,len(data)-1)
    
  
    return {"data": sorted_data}