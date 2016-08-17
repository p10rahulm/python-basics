from random import randint
counter = 0

def quickSort(listA):
    quickSortHelper(listA,0,len(listA)-1)

def quickSortHelper(listA,indexstart,indexend):
    if indexstart >= indexend: return
    splitpoint = partition(listA,indexstart,indexend)
    quickSortHelper(listA,indexstart,splitpoint-1)
    quickSortHelper(listA,splitpoint+1,indexend)

def randomtofirst(listA,indexstart,indexend):
    p = randint(indexstart,indexend)
    temp = listA[indexstart]
    listA[indexstart] = listA[p]
    listA[p] = temp
    return

def swap(ArrayMod,index1,index2):
    temp = ArrayMod[index1]
    ArrayMod[index1] = ArrayMod[index2]
    ArrayMod[index2] = temp

def swapmedianwithstart(listA,indexstart,indexend):
    lowest = listA[indexstart]
    highest = listA[indexend]
    middle = listA[indexstart + int((indexend-indexstart)/2)]
    if (lowest < middle and middle < highest) or (highest <middle and middle < lowest):
        swap(listA,indexstart,indexstart + int((indexend-indexstart)/2))
    elif (lowest < highest and highest < middle) or (middle < highest and highest < lowest):
        swap(listA,indexstart,indexend)
    return

def partition(listA,indexstart,indexend):
    #swapping with random is a goodroutine and improves upon taking first element
    #randomtofirst(listA,indexstart,indexend)
    #swapping with median of first, middle and last element works for already almost sorted arrays
    #swapmedianwithstart(listA,indexstart,indexend)
    #swap last with first
    swap(listA,indexend,indexstart)
    pivotvalue = listA[indexstart]
    indexLeft = indexstart+1
    indexRight = indexend
    #counts number of comparisons
    global counter
    for j in range(indexLeft,indexRight+1):
        counter+=1
        if listA[j] < pivotvalue:
            swap(listA,indexLeft,j)
            indexLeft+=1

    swap(listA,indexstart,indexLeft-1)
    return indexLeft-1
'''
# Below uses while loop instead of for loop in partition
    def partition(listA,indexstart,indexend):
        randomtofirst(listA,indexstart,indexend)
        pivotvalue = listA[indexstart]
        indexLeft = indexstart+1
        indexRight = indexend
        done = False
        while not done:
            while indexLeft <= indexRight and listA[indexLeft] <= pivotvalue:
                indexLeft = indexLeft + 1
            while listA[indexRight] >= pivotvalue and indexRight >= indexLeft:
                indexRight = indexRight -1
            if indexRight < indexLeft:
                done = True
            else:
                temp = listA[indexLeft]
                listA[indexLeft] = listA[indexRight]
                listA[indexRight] = temp

        temp = listA[indexstart]
        listA[indexstart] = listA[indexRight]
        listA[indexRight] = temp


        return indexRight
'''

if __name__ == "__main__":
    #test 1
    from openfile import openfile_returnlist
    filename = "data/countqsortdata.txt"
    data = openfile_returnlist(filename)
    quickSort(data)
    print("data10 = ",data[:10])
    print(counter)




    listA = [54,26,93,17,77,31,44,55,20]
    quickSort(listA)
    print(listA)

    listA = [1,2,3,1,6,2,100,1]
    quickSort(listA)
    print(listA)

    import time
    start_time = time.time()
    listA = list(range(100,0,-1))
    quickSort(listA)
    print(listA[0:10])
    print("--- %s seconds ---" % (time.time() - start_time))

    from Mergesort import mergesorts
    start_time = time.time()
    listA = list(range(100,0,-1))
    print(mergesorts(listA)[0:10])
    print("--- %s seconds ---" % (time.time() - start_time))

