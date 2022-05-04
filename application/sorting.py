from copy import deepcopy
from application import heap

# Define sorting functions here
def heapSort(data, sort_by):
    heap.buildMaxHeap(data, sort_by)

    sorted_data = []

    for i in range(len(data)):
        sorted_data.append(heap.extractMin(data, sort_by))

    return sorted_data

# Radix Sort for Strings
def getMaximumString(n):
    max = len(n[0]['name'])
    for i in range(len(n)):
        if max < len(n[i]['name']):
            max = len(n[i]['name'])
    return max

def getPlaceString(n, digit):
    if len(n) < digit:
        return ord(n[0])
    else: 
        return ord(n[len(n) - 1 - digit])

def bucketSortString(n, currentDigit):
    # 150 is far past the ASCII maximum for last letter 'Z'
    count = [0 for i in range(150)]

    for i in range(len(n)):
        count[getPlaceString(n[i]['name'], currentDigit)] += 1
    
    for i in range(1, len(count)):
        count[i] += count[i - 1]

    sorted = [0 for i in range(len(n))]
    for i in reversed(range(len(n))):
        sorted[count[getPlaceString(n[i]['name'], currentDigit)] - 1] = n[i]
        count[getPlaceString(n[i]['name'], currentDigit)] -= 1

    return sorted

def radixSortString(n):
    # With string, use string length instead of max digits of a number
    l = getMaximumString(n)
    numDigits = l

    for i in range(len(n)):
        length = len(n[i]['name'])
        if length < numDigits:
            n[i]['name'] = n[i]['name'].ljust(numDigits, '(')

    currentDigit = 0
    sorted = n
    while currentDigit < numDigits:
        sorted = bucketSortString(sorted, currentDigit)
        currentDigit += 1

    for i in range(len(n)):
        n[i]['name'] = n[i]['name'][0:n[i]['name'].find('(')]

    return sorted


# Radix Sort for Prices
def getMaximumPrice(n):
    max = n[0]['price']
    for i in range(len(n)):
        if max < n[i]['price']:
            max = n[i]['price']
    return max

def getPlaceDigit(n, digit):
    return int((n / (10 ** digit)) % 10)

def bucketSortPrice(n, currentDigit):
    count = [0 for i in range(10)]

    for i in range(len(n)):
        count[getPlaceDigit(n[i]['price'], currentDigit)] += 1
    
    for i in range(1, len(count)):
        count[i] += count[i - 1]

    sorted = [0 for i in range(len(n))]
    for i in reversed(range(len(n))):
        sorted[count[getPlaceDigit(n[i]['price'], currentDigit)] - 1] = n[i]
        count[getPlaceDigit(n[i]['price'], currentDigit)] -= 1

    return sorted

def radixSortPrice(n):
    # Radixsort with decimals not valid, so convert to integer (cents only)
    for i in range(len(n)):
        n[i]['price'] = n[i]['price'] * 100
    
    l = getMaximumPrice(n)
    numDigits = 0
    temp = l
    while temp > 0:
        temp = int(temp / 10)
        numDigits += 1

    currentDigit = 0
    sorted = n
    while currentDigit < numDigits:
        sorted = bucketSortPrice(sorted, currentDigit)
        currentDigit += 1

    # Reconvert back to decimal values (actual price in dollars and cents)
    for i in range(len(sorted)):
        sorted[i]['price'] = sorted[i]['price'] / 100
        
    return sorted