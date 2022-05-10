
from flask import render_template, flash, redirect, session, json, request
from application import app
import os
from application import sorting
from copy import deepcopy
import time
import random

import sys
import matplotlib.pyplot as plt


sys.setrecursionlimit(1000000)

@app.route('/confirm',methods=['GET','POST'])
def confirm():
    print("Here")
    return render_template("confirm.html")

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

def insertionSortbyName(arr, sort_by):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        while j >= 0 and key['name'] < arr[j]['name'] :
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def insertionSortbyPrice(arr, sort_by):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        while j >= 0 and key['price'] < arr[j]['price'] :
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def hybridSortName(arr, l, r):
    total_dataset_size = len(arr)
    if total_dataset_size < 3000:
        return quickSortbyName(arr, l, r)
    else:
        return mergeSortbyName(arr, l, r)

def hybridSortPrice(arr, l, r):
    total_dataset_size = len(arr)
    if total_dataset_size < 3000:
        return quickSortbyPrice(arr, l, r)
    elif total_dataset_size < 6000:
        return mergeSortbyPrice(arr, l, r)
    else:
        return sorting.radixSortPrice(arr)

@app.route("/reload", methods=['GET', 'POST'])
def reload():
    filename = os.path.join(app.static_folder, 'data', 'products.json')
    global product_data
    with open(filename) as file:
        product_data = json.load(file)

    non_duplicate_amount = len(product_data)

    display_amount = round(non_duplicate_amount * float(request.args.get('by')))
    curr_id = non_duplicate_amount + 1

    new_data = []

    for i in range(display_amount):
        new_product = product_data[i % non_duplicate_amount].copy()
        new_product['id'] = curr_id
        curr_id += 1
        new_data.append(new_product)

    product_data = new_data
    random.shuffle(product_data)

    return {'data': product_data}

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
    elif sort_type == "hybridsort":
        if sort_by == "name":
            start = time.perf_counter_ns()
            sorted_data = hybridSortName(data, 0, len(data) - 1)
            end = time.perf_counter_ns()
        elif sort_by == "price":
            start = time.perf_counter_ns()
            sorted_data = hybridSortPrice(data, 0, len(data) - 1)
            end = time.perf_counter_ns()

    delta = (end - start)

    return {'data': sorted_data, 'time': delta}

@app.route("/comparepage", methods=['GET', 'POST'])
def comparepage():
    return render_template("comparison.html")

def plot(x, data):
    sort_map = ["quicksort", "mergesort", "insertionsort", "heapsort", "radixsort", "hybridsort"]
    colors = ["r", "g", "c", "b", "y", "m"]
    for i in range(len(data)):
        plt.plot(x, data[i][0], linestyle="-", linewidth=1.5, color=colors[i], label=sort_map[i].capitalize() + " by Name")
        plt.plot(x, data[i][1], linestyle="--", linewidth=1, color=colors[i], label=sort_map[i].capitalize() + " by Price")
    plt.legend(loc='upper left')
    plt.xlabel("Dataset Size (# of products)")
    plt.ylabel("Running Time (milliseconds)")
    plt.title("Comparison of Various Sorting Algorithms")
    plt.show()

def plotLarge(x, data):
    sort_map = ["quicksort", "mergesort", "insertionsort", "heapsort", "radixsort", "hybridsort"]
    colors = ["r", "g", "c", "b", "y", "m"]
    for i in range(len(data)):
        plt.plot(x, data[i][0], linestyle="-", linewidth=1.5, color=colors[i], label=sort_map[i].capitalize() + " by Name")
        plt.plot(x, data[i][1], linestyle="--", linewidth=1, color=colors[i], label=sort_map[i].capitalize() + " by Price")
    plt.legend(loc='upper left')
    plt.xlabel("Dataset Size (# of products)")
    plt.ylabel("Running Time (milliseconds)")
    plt.title("Comparison of Various Sorting Algorithms")
    plt.show()

@app.route("/compare", methods=['GET', 'POST'])
def compare():

    print("Starting Comparisons...")


    by_amount = [0.25, 0.5, 0.75, 1, 1.5, 2, 4, 8, 10, 25] # Used for the small datasets, include 50 (takes longer)
    #by_amount = [0.25, 0.5, 0.75, 1, 1.5, 2, 4, 8, 10, 25, 50, 75, 100, 250, 500] # use for large dataset
    #by_amount = [0.25, 0.5, 0.75, 1] # use for non-duplicate data

    all_sort_times = [
        [[], []],
        [[], []],
        [[], []],
        [[], []],
        [[], []],
        [[], []]
    ]

    dataset_amounts = []

    for factor in range(len(by_amount)):
        filename = os.path.join(app.static_folder, 'data', 'products.json')
        global product_data
        with open(filename) as file:
            product_data = json.load(file)
        non_duplicate_amount = len(product_data)

        display_amount = round(non_duplicate_amount * float(by_amount[factor]))
        dataset_amounts.append(display_amount)
        curr_id = non_duplicate_amount + 1

        new_data = []

        # Create the new dataset using the original dataset (either duplicate or take a fraction of)
        for k in range(display_amount):
            new_product = product_data[k % non_duplicate_amount].copy()
            new_product['id'] = curr_id
            curr_id += 1
            new_data.append(new_product)

        product_data = new_data

        # Randomly shuffle dataset for fairness
        random.shuffle(product_data)

        sort_map = ["quicksort", "mergesort", "insertionsort", "heapsort", "radixsort", "hybridsort"]
        sort_by_type_map = ["name", "price"]
        num_trials = 10

        # Run all sorting trials using the product dataset, do not modify, just deepcopy it.
        for i in range(len(sort_map)):
            for j in range(len(sort_by_type_map)):
                trials = 0
                for l in range(num_trials):
                    data = deepcopy(product_data)

                    sort_type = sort_map[i]
                    sort_by = sort_by_type_map[j]

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
                    elif sort_type == "hybridsort":
                        if sort_by == "name":
                            start = time.perf_counter_ns()
                            sorted_data = hybridSortName(data, 0, len(data) - 1)
                            end = time.perf_counter_ns()
                        elif sort_by == "price":
                            start = time.perf_counter_ns()
                            sorted_data = hybridSortPrice(data, 0, len(data) - 1)
                            end = time.perf_counter_ns()

                    delta = (end - start)
                    trials += delta

                # Convert to ms from ns
                average_ms = (trials / num_trials) / 1000000
                all_sort_times[i][j].append(average_ms)

        # Debug
        print("Dataset: ", by_amount[factor])

    # Plot graph
    plot(dataset_amounts, all_sort_times)
    return {'data': None}
