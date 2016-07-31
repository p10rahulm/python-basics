def mergesortncount(mylist):
    sz = len(mylist[0])
    if sz == 1:
        mylist[1]=0
        return mylist
    if sz%2 ==0: k = sz/2
    else: k = (sz+1)/2
    k = int(k)
    return mergesncounts(mergesortncount([mylist[0][:k],mylist[1]]),mergesortncount([mylist[0][k:],0]))


def mergesncounts(flistA,flistB):
    listk = [[0 for i in range(len(flistA[0])+len(flistB[0]))],0]
    listk[1] += flistA[1]+flistB[1]
    listA = flistA[0]
    listB = flistB[0]
    i=0
    j=0
    for k in range(len(listA)+len(listB)):
        if j >= (len(listB)):
            listk[0][k] = listA[i]
            i+=1
        elif i >= (len(listA)):
            listk[0][k] = listB[j]
            j+=1
        elif listA[i] <= listB[j]:
            listk[0][k] = listA[i]
            i+=1
        elif listB[j] < listA[i]:
            listk[0][k] = listB[j]
            listk[1]+= len(listA)- i
            j+=1
    return listk

if __name__ == "__main__":
    from openfile import openfile_returnlist
    filename = "data/CountInversionsData.txt"
    data = openfile_returnlist(filename)
    print("Checking the number of inversions in the file ",filename)
    print(mergesortncount([data,0])[1])


    #some checks
    A = [[8,4,1,6,7,2,6,2,2221],0]
    print("A = ",A,"\nmerges = " , mergesortncount(A))
    A = [[1,2,3],0]
    print("A = ",A,"\nmerges = " , mergesortncount(A))
    A = [[3,2,1],0]
    print("A = ",A,"\nmerges = " , mergesortncount(A))
    A = [[2,1],0]
    print("A = ",A,"\nmerges = " , mergesortncount(A))
    A = [[2,1,3],0]
    print("A = ",A,"\nmerges = " , mergesortncount(A))
    A = [[3,1,3],0]
    print("A = ",A,"\nmerges = " , mergesortncount(A))
    A = [[3,3,3],0]
    print("A = ",A,"\nmerges = " , mergesortncount(A))
    A = [[3,3,3,-2,-1,0],0]
    print("A = ",A,"\nmerges = " , mergesortncount(A))
