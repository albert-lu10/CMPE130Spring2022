# Implementation of a heap using only functions (must manually provide the array and custom designed to accept a specific JSON data key (i.e. 'name')))
def insert(arr, x, sort_by):
    arr.append(x)
    current_pos = int((len(arr) - 1) / 2 - 1)
    while current_pos >= 0 and arr[current_pos][sort_by] > x[sort_by]:
        minHeapify(arr, current_pos)
        current_pos = int((current_pos / 2) - 1)

def minHeapify(arr, x, sort_by):
    x = int(x)
    lowest = x
    if 2 * x + 1 <= (len(arr) - 1) and arr[lowest][sort_by] > arr[2 * x + 1][sort_by]:
        # Left
        lowest = 2 * x + 1
    if 2 * x + 2 <= (len(arr) - 1) and arr[lowest][sort_by] > arr[2 * x + 2][sort_by]:
        # Right
        lowest = 2 * x + 2

    if lowest != x:
        temp = arr[lowest]
        arr[lowest] = arr[x]
        arr[x] = temp
        minHeapify(arr, lowest, sort_by)

def extractMin(arr, sort_by):
    if len(arr) <= 0:
        return
    max = arr[0]

    temp = arr[0]
    arr[0] = arr[len(arr) - 1]
    arr[len(arr) - 1] = temp

    arr.pop()

    minHeapify(arr, 0, sort_by)

    return max
    
def buildMaxHeap(arr, sort_by):
    for i in reversed(range(int(len(arr) / 2))):
        minHeapify(arr, i, sort_by)