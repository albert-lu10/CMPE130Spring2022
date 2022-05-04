
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

def merge1(arr, l, m, r):
    item1=m-l+1
    n1=str(item1["name"])
    item2=r-m
    n2 = str(item2["name"])
 
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
    