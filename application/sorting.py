from copy import deepcopy
from application import heap

# Define sorting functions here
def heapSort(data, sort_by):
    heap.buildMaxHeap(data, sort_by)

    sorted_data = []

    for i in range(len(data)):
        sorted_data.append(heap.extractMin(data, sort_by))

    return sorted_data