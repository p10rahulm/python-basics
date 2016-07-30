from random import randint

def RSelect(Arraylist,length,order):
    return RSelectFunc(Arraylist,0,len(Arraylist)-1,order-1)

def RSelectFunc(Arraylist,startindex,endindex,order):
    if len(Arraylist) == 1: return A[0]
    if startindex == endindex: return A[startindex]
    #Choose pivot
    p = partition(Arraylist,startindex,endindex)
    if p == order: return Arraylist[order]
    elif p> order: return RSelectFunc(Arraylist,startindex,p-1,order)
    else: return RSelectFunc(Arraylist,p+1,endindex,order)


def partition(listA,indexstart,indexend):
    #swapping with random is a goodroutine and improves upon taking first element
    randomtofirst(listA,indexstart,indexend)
    #swapping with median of first, middle and last element works for already almost sorted arrays
    #swapmedianwithstart(listA,indexstart,indexend)
    pivotvalue = listA[indexstart]
    indexLeft = indexstart+1
    indexRight = indexend
    #counts number of comparisons
    for j in range(indexLeft,indexRight+1):
        if listA[j] <= pivotvalue:
            swap(listA,indexLeft,j)
            indexLeft+=1

    swap(listA,indexstart,indexLeft-1)
    return indexLeft-1

def randomtofirst(listA,indexstart,indexend):
    #print("listA = ",listA,"indexstart = ",indexstart,"indexend = ", indexend)
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

# Tests-----------
A = [3,2,1,4,1,1]
bool = False
for i in range(10000):
    if RSelect(A,len(A),1) != 1: bool = True
    if RSelect(A,len(A),2) != 1: bool = True
    if RSelect(A,len(A),3) != 1: bool = True
    if RSelect(A,len(A),4) != 2: bool = True
    if RSelect(A,len(A),5) != 3: bool = True
    if RSelect(A,len(A),6) != 4: bool = True

if bool == True: print("Problem")
else: print("all ok!")