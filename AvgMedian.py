from MergeSort import mergesorts

def nth_element_in_list(listA,n):
    #print(listA,n)
    if len(listA) <=5:
        return mergesorts(listA)[n]
    k = int(len(listA)/2)
    listMatrix = [[0 for i in range(5)] for j in range(int((len(listA)+4)/5))]

    for i in range(len(listA)):
        listMatrix[int(i/5)][i%5] = listA[i]
    medianslist = [0 for i in range(len(listMatrix))]
    for i in range(len(listMatrix)):
        medianslist[i] = mergesorts(listMatrix[i])[2]
    medianofmedians = nth_element_in_list(medianslist,int(len(medianslist)/2))
    L  = []
    R = []
    for i in range(len(listA)):
        if listA[i] < medianofmedians:
            L.append(listA[i])
        else:
            R.append(listA[i])
    R.remove(medianofmedians)
    r = len(L)+1
    if n == r-1:
        return medianofmedians
    elif n < r-1:
        return nth_element_in_list(L,n)
    else:
        return nth_element_in_list(R,n-r)

    #print(listMatrix,medianslist,medianofmedians)


def average(listA):
    sum=0
    for i in range(len(listA)):
        sum +=listA[i]
    return sum/len(listA)


'''
A = [1,2,3,4,5,6,7,8,9,10]
n=int(len(A)/2)
print("A = \n", A,"\nn = ",n,"\nnth_element_in_list =",nth_element_in_list(A,n))

A = [1,2,3,4,5,6,7,8,9,10]
n=1
print("A = \n", A,"\nn = ",n,"\nnth_element_in_list =",nth_element_in_list(A,n))

A = [1,2,3,4,5,6,7,8,9,10]
n=2
print("A = \n", A,"\nn = ",n,"\nnth_element_in_list =",nth_element_in_list(A,n))

A = [1,2,3,4,5,6,7,8,9,10]
n=3
print("A = \n", A,"\nn = ",n,"\nnth_element_in_list =",nth_element_in_list(A,n))


A = [1,2,3,4,5,6,7,8,9,10]
n=4
print("A = \n", A,"\nn = ",n,"\nnth_element_in_list =",nth_element_in_list(A,n))


A = [1,2,3,4,5,6,7,8,9,10]
n=5
print("A = \n", A,"\nn = ",n,"\nnth_element_in_list =",nth_element_in_list(A,n))
'''
