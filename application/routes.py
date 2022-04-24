from flask import render_template, flash, redirect, session, json
from application import app
import os
from application import sorting
from copy import deepcopy

product_data = None

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

def mergeSort():
    print("Do Mergesort")

def insertionSort():
    print("Do Insertion Sort")

@app.route('/quicksortbyname', methods=['GET', 'POST'])
def quicksort_by_name():
    global product_data
    data = deepcopy(product_data)
        
    sorted_data = quickSortbyName(data,0,len(data)-1)
    return {'data': sorted_data}

@app.route('/quicksortbyprice', methods=['GET', 'POST'])
def quicksort_by_price():
    global product_data
    data = deepcopy(product_data)
        
    sorted_data = quickSortbyPrice(data,0,len(data)-1)
    return {'data': sorted_data}

@app.route('/mergesortbyname', methods=['GET', 'POST'])
def mergesort_by_name():
    global product_data
    data = deepcopy(product_data)

    print("Begin mergesort")
    sorted_data = mergeSort()
    return {'data': sorted_data}

@app.route('/mergesortbyname', methods=['GET', 'POST'])
def mergesort_by_price():
    global product_data
    data = deepcopy(product_data)

    print("Begin mergesort")
    sorted_data = mergeSort()
    return {'data': sorted_data}

@app.route('/insertionsortbyname', methods=['GET', 'POST'])
def insertionsort_by_name():
    global product_data
    data = deepcopy(product_data)

    print("Begin insertionsort")
    sorted_data = insertionSort()

    return {'data': sorted_data}

@app.route('/insertionsortbyprice', methods=['GET', 'POST'])
def insertionsort_by_price():
    global product_data
    data = deepcopy(product_data)

    print("Begin insertionsort")
    sorted_data = insertionSort()

    return {'data': sorted_data}

@app.route('/heapsortbyname', methods=['GET', 'POST'])
def heapsort_by_name():
    global product_data
    data = deepcopy(product_data)

    print("Begin HeapSort")

    sorted_data = sorting.heapSort(data, 'name')

    return {'data': sorted_data}

@app.route('/heapsortbyprice', methods=['GET', 'POST'])
def heapsort_by_price():
    global product_data
    data = deepcopy(product_data)

    print("Begin HeapSort")

    sorted_data = sorting.heapSort(data, 'price')

    return {'data': sorted_data}