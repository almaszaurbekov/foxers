import time
import init

# Search by N
def linearSearch(arr, personName):
    for i in range(1, len(arr)):
        print("index: {}".format(i))
        if arr[i][0] == personName:
            print("Success!")
            init.showCitizen(i)
            break
        else:
            print("Failed...")
        time.sleep(1)

# Search by log(n)
# Key is convertedNumber from init
def binarySearchWithoutRecursion(arr, key):
    # Start from 1, because rows[0] is fieldname
    start = 1
    end = len(arr)
    while(start < end):
        mid = (start + end) // 2
        value = init.convertNumber(arr[mid][1])
        print("rows[{}]".format(mid))
        if(key == value):
            print("Success!")
            init.showCitizen(mid)
            return mid
        elif(key > value):
            print("Failed, have turned to the right...")
            start = mid
        elif(key < value):
            print("Failed, have turned to the left...")
            end = mid
        time.sleep(1)
    return 0

# Search by log(n)
def binarySearchWithRecursion(arr, key):
    start = 1
    end = len(arr)
    init.showCitizen(bsRecursion(arr, start, end, key))

def bsRecursion(arr, start, end, key):
    mid = (start + end) // 2
    value = init.convertNumber(arr[mid][1])

    time.sleep(1)
    print("rows[{}]".format(mid))
    if(key == value):
        print("Success!")
        return mid
    elif(key > value):
        print("Failed, have turned to the right...")
        return bsRecursion(arr, mid, end, key)
    elif(key < value):
        print("Failed, have turned to the left...")
        return bsRecursion(arr, start, mid, key)

# Sort by log(n)
def quickSortWithRecursion(arr, start, end):
    if(start >= end):
        return
    pivot = partition(arr, start, end)
    quickSortWithRecursion(arr, start, pivot - 1)
    quickSortWithRecursion(arr, pivot + 1, end)


def partition(arr, start, end):
    marker = start
    for i in range(start, end):
        if(arr[i] < arr[end]):
            arr[marker], arr[i] = arr[i], arr[marker]
            marker+=1
    arr[marker], arr[end] = arr[end], arr[marker]
    return marker