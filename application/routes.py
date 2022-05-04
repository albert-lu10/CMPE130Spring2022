
from flask import render_template, flash, redirect, session, json, request
from application import app
import os
from application import sorting
from copy import deepcopy

product_data = None
@app.route('/checkout',methods=['GET','POST'])
def checkout():
    return render_template("checkout.html")

@app.route("/")
@app.route("/home")
def index():
    filename = os.path.join(app.static_folder, 'data', 'products.json')
    global product_data
    with open(filename) as file:
        product_data = json.load(file)
    return render_template("index.html", data=product_data)

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

    
def insertionSortbyName():
    print("Do Insertion Sort")

def insertionSortbyPrice():
    print("Do Insertion Sort")

@app.route('/sort', methods=['GET', 'POST'])
def sort():
    global product_data
    data = deepcopy(product_data)
    
    sort_type = request.args.get('type')
    sort_by = request.args.get('by')

    sorted_data = []

    if sort_type == "quicksort":
        if sort_by == "name":
            sorted_data = quickSortbyName(data,0,len(data)-1)
        elif sort_by == "price":
            sorted_data = quickSortbyPrice(data,0,len(data)-1)
    elif sort_type == "mergesort":
        if sort_by == "name":
            sorted_data = mergeSortbyName(data, 0, len(data) -1)
        elif sort_by == "price":
            sorted_data = mergeSortbyPrice(data, 0, len(data) - 1)
    elif sort_type == "insertionsort":
        if sort_by == "name":
            sorted_data = insertionSortbyName(data, 'name')
        elif sort_by == "price":
            sorted_data = insertionSortbyPrice(data, 'price')
    elif sort_type == "heapsort":
        if sort_by == "name":
            sorted_data = sorting.heapSort(data, 'name')
        elif sort_by == "price":
            sorted_data = sorting.heapSort(data, 'price')
    
    return {'data': sorted_data}
    
