def mergesorts(mylist):
    sz = len(mylist)
    if sz == 1:
        return mylist
    if sz%2 ==0: k = sz/2
    else: k = (sz+1)/2
    k = int(k)
    #print(k)
    return merges(mergesorts(mylist[:k]),mergesorts(mylist[k:]))


def merges(listA,listB):
    listk = [0 for i in range(len(listA)+len(listB))]
    #print(listA)
    #print(listB)
    i=0
    j=0
    for k in range(len(listA)+len(listB)):
        if j >= (len(listB)):
            #print("i="+ str(i) +"j = " + str(j) + "k=" + str(k))
            listk[k] = listA[i]
            i+=1
        elif i >= (len(listA)):
            #print("i="+ str(i) +"j = " + str(j) + "k=" + str(k))
            listk[k] = listB[j]
            j+=1
        elif listA[i] <= listB[j]:
            #print("i="+ str(i) +"j = " + str(j) + "k=" + str(k))
            listk[k] = listA[i]
            i+=1
        elif listB[j] < listA[i]:
            #print("i="+ str(i) +"j = " + str(j) + "k=" + str(k))
            listk[k] = listB[j]
            j+=1
    return listk

#A = [8,4,1,6,7,2,6,2,2221]
#print(mergesorts(A))

#return list2 sorted by mylist
def mergesorttwolists(mylist,list2):
    sz = len(mylist)
    if sz == 1:
        return mylist,list2
    if sz%2 ==0: k = sz/2
    else: k = (sz+1)/2
    k = int(k)
    #print(k)
    list1, slist1 = mergesorttwolists(mylist[:k],list2[:k])
    list2, slist2 = mergesorttwolists(mylist[k:],list2[k:])
    return merges_list_and_sortlist(list1,list2,slist1,slist2)


def merges_list_and_sortlist(listA,listB,sortlistA,sortlistB):
    listk = [0 for i in range(len(listA)+len(listB))]
    sortlistk = [0 for i in range(len(listA)+len(listB))]
    #print(listA)
    #print(listB)
    i=0
    j=0
    for k in range(len(listA)+len(listB)):
        if j >= (len(listB)):
            #print("i="+ str(i) +"j = " + str(j) + "k=" + str(k))
            listk[k] = listA[i]
            sortlistk[k] = sortlistA[i]
            i+=1
        elif i >= (len(listA)):
            #print("i="+ str(i) +"j = " + str(j) + "k=" + str(k))
            listk[k] = listB[j]
            sortlistk[k] = sortlistB[j]
            j+=1
        elif listA[i] <= listB[j]:
            #print("i="+ str(i) +"j = " + str(j) + "k=" + str(k))
            listk[k] = listA[i]
            sortlistk[k] = sortlistA[i]
            i+=1
        elif listB[j] < listA[i]:
            #print("i="+ str(i) +"j = " + str(j) + "k=" + str(k))
            listk[k] = listB[j]
            sortlistk[k] = sortlistB[j]
            j+=1
    return listk,sortlistk

'''
A = [8,4,1,6,7,2,6,2,2221]
print(mergesorts(A))

A = [1,2,3,4,5,6,7,8,10,9]
B = [10,9,8,7,6,5,4,3,2,1]
print("A = \n" , A , "\nB = ",B,"\nMerged and sorted lists are\n" , mergesorttwolists(A,B))
'''