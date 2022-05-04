
from flask import render_template, flash, redirect, session, json, request
from application import app
import os
from application import sorting
from copy import deepcopy
import time

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
  
def merge1(arr, l, m, r): 
    n1 = m - l + 1
    n2 = r - m

    L = [0] * (n1)
    R = [0] * (n2)

    for i in range(0, n1):
        L[i] = arr[l + i]
    
    for j in range(0, n2):
        R[j] = arr[m + 1 + j]

    i = 0     
    j = 0     
    k = l     

    while i < n1 and j < n2:
        if L[i]["name"] <= R[j]["name"]:
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

def mergeSortbyName(arr, l, r):
    if l < r:
        m = l+(r-l)//2
        mergeSortbyName(arr, l, m)
        mergeSortbyName(arr, m+1, r)
        merge1(arr, l, m, r)
    return arr

def merge2(arr, l, m, r):
    n1 = m-l+1
    n2 = r-m
 
    L = [0] * (n1)
    R = [0] * (n2)

    for i in range(0, n1):
        L[i] = arr[l + i]
 
    for j in range(0, n2):
        R[j] = arr[m + 1 + j]
 
    i = 0     
    j = 0     
    k = l     

    while i < n1 and j < n2:
        if L[i]["price"] <= R[j]["price"]:
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

def mergeSortbyPrice(arr, l, r):
    if l < r:
        m = l+(r-l)//2
        mergeSortbyPrice(arr, l, m)
        mergeSortbyPrice(arr, m+1, r)
        merge2(arr, l, m, r)
    return arr
    
@app.route('/sortbyname', methods=['GET', 'POST'])


def mergeSortbyName():
    print("Do Mergesort")

def mergeSortbyPrice():
    print("Do Mergesort")

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

    start = 0
    end = 0

    if sort_type == "quicksort":
        if sort_by == "name":
            start = time.perf_counter_ns()
            sorted_data = quickSortbyName(data,0,len(data)-1)
            end = time.perf_counter_ns()
        elif sort_by == "price":
            start = time.perf_counter_ns()
            sorted_data = quickSortbyPrice(data,0,len(data)-1)
            end = time.perf_counter_ns()
    elif sort_type == "mergesort":
        if sort_by == "name":
            start = time.perf_counter_ns()
            sorted_data = mergeSortbyName(data, 0, len(data) -1)
            end = time.perf_counter_ns()
        elif sort_by == "price":
            start = time.perf_counter_ns()
            sorted_data = mergeSortbyPrice(data, 0, len(data) - 1)
            end = time.perf_counter_ns()
    elif sort_type == "insertionsort":
        if sort_by == "name":
            start = time.perf_counter_ns()
            sorted_data = insertionSortbyName(data, 'name')
            end = time.perf_counter_ns()
        elif sort_by == "price":
            start = time.perf_counter_ns()
            sorted_data = insertionSortbyPrice(data, 'price')
            end = time.perf_counter_ns()
    elif sort_type == "heapsort":
        if sort_by == "name":
            start = time.perf_counter_ns()
            sorted_data = sorting.heapSort(data, 'name')
            end = time.perf_counter_ns()
        elif sort_by == "price":
            start = time.perf_counter_ns()
            sorted_data = sorting.heapSort(data, 'price')
            end = time.perf_counter_ns()
    elif sort_type == "radixsort":
        if sort_by == "name":
            start = time.perf_counter_ns()
            sorted_data = sorting.radixSortString(data)
            end = time.perf_counter_ns()
        elif sort_by == "price":
            start = time.perf_counter_ns()
            sorted_data = sorting.radixSortPrice(data)
            end = time.perf_counter_ns()
    
    delta = (end - start)

    return {'data': sorted_data, 'time': delta}
    
