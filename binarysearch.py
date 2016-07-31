def binarysearchfound(sortedarray,value):
    a = len(sortedarray)
    if a ==1:
        if sortedarray[0] == value: return True
        else: return False
    elif a ==0: return False
    k = int(a/2)
    if sortedarray[k] ==value:
        return True
    elif sortedarray[k] > value:
        return binarysearchfound(sortedarray[:k],value)
    else: return binarysearchfound(sortedarray[k:],value)

def binarysearch_return_index(sortedarray,value,indexstart):
    a = len(sortedarray)
    if a ==1:
        if sortedarray[0] == value: return indexstart
        else: return False
    elif a ==0: return False
    k = int(a/2)
    if sortedarray[k] ==value:
        return indexstart + k
    elif sortedarray[k] > value:
        return binarysearch_return_index(sortedarray[:k],value,indexstart)
    else: return binarysearch_return_index(sortedarray[k+1:],value,indexstart+k+1)

def binarysearch(sortedarray,value):
    return binarysearch_return_index(sortedarray,value,0)

if __name__ == "__main__":
    A = []
    value = 2
    print("A = ",A,"value = ",value,"found value in array? ",binarysearchfound(A,value),"index = ", binarysearch(A,value))
    A = [1,2,3,4,5]
    value = 1.5
    print("A = ",A,"value = ",value,"found value in array? ",binarysearchfound(A,value),"index = ", binarysearch(A,value))
    A = [1,2,3,4,5]
    value = 7
    print("A = ",A,"value = ",value,"found value in array? ",binarysearchfound(A,value),"index = ", binarysearch(A,value))
    A = [1,2,3,4,5]
    value = 1
    print("A = ",A,"value = ",value,"found value in array? ",binarysearchfound(A,value),"index = ", binarysearch(A,value))
    A = [1,1,1,1,1]
    value = 1
    print("A = ",A,"value = ",value,"found value in array? ",binarysearchfound(A,value),"index = ", binarysearch(A,value))