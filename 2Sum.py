from quicksort import quickSort
from binarysearch import binarysearchLowerThanorEqual

#PLEASE USE THE THIRD METHOD FOR TEST CASE


def sumofTwoBetween(inputList,fromTarget,toTarget,distinct = False):
    inputlistlen = len(inputList)
    targetnum = []
    for i in range(len(inputList)):
        firstnum = inputList[i]
        lowerboundonsecondnum = fromTarget - firstnum
        lowerindex = binarysearchLowerThanorEqual(inputList,lowerboundonsecondnum)
        if lowerindex is False or lowerindex is None: continue
        #if lowerindex >= len(inputList): continue
        upperboundonsecondnum = toTarget - firstnum
        j = 0
        while lowerindex + j > i and inputList[lowerindex + j] <= upperboundonsecondnum:
            if (firstnum + inputList[lowerindex + j]) <= toTarget and \
                (firstnum + inputList[lowerindex + j]) >= fromTarget:
                targetnum.append((firstnum+inputList[lowerindex+j],firstnum,inputList[lowerindex+j]))
            j+=1
            if lowerindex + j >= inputlistlen:break
        if i%100 == 0: print(i/10000,"percent complete")
    return targetnum

def sumofTwoBetweenusingdict(inputList,fromTarget,toTarget,distinct = False):
    g = {}
    for i in inputList:
        g[i] = None
    inputlistlen = len(inputList)
    targetnum = []
    loopscomplete = 0
    for i in g:
        firstnum = i
        lowerboundonsecondnum = fromTarget - firstnum
        upperboundonsecondnum = toTarget - firstnum
        for j in range(lowerboundonsecondnum,upperboundonsecondnum+1):
            if j in g:
                targetnum.append((firstnum+j,firstnum,j))
        loopscomplete +=1
        if loopscomplete%1000 == 0: print(loopscomplete/10000,"percent complete")

    return targetnum


def sum2betweenwith2lists(poslist,neglist,upperbound,lowerbound,lenpos,lenneg):
    posptr = 0
    negptr = 0
    negiter = 0
    target = set()
    while posptr < lenpos and negptr < lenneg:
        sumtwo = poslist[posptr] + neglist[negptr]
        if sumtwo > upperbound:
            posptr +=1
            continue
        if sumtwo < lowerbound:
            negptr +=1
            continue
        iterator = 0
        while poslist[posptr] + neglist[negptr +iterator] <= upperbound:
            target.add(poslist[posptr] + neglist[negptr +iterator])
            iterator +=1
        posptr +=1
    return target




def sumTwoBetweenwithPosNegLists(poslist,neglist,upperbound,lowerbound):
    posptr = 0
    negptr = 0
    target = []
    numloops = 0
    lenpos = len(poslist)
    lenneg = len(neglist)
    while posptr < lenpos and negptr < lenneg:
        currposptr = 0
        while neglist[negptr] + poslist[posptr+currposptr] >= lowerbound:
            if currposptr ==0:
                if neglist[negptr] + poslist[posptr+currposptr] >= upperbound:
                    if posptr + currposptr + 1 < lenpos:
                        posptr +=1
                    else:
                        break
            if neglist[negptr] + poslist[posptr+currposptr] <=upperbound:
                if neglist[negptr] + poslist[posptr+currposptr]>=lowerbound:
                    target.append((neglist[negptr] + poslist[posptr+currposptr], neglist[negptr], poslist[posptr+currposptr]))
            if (posptr+currposptr+1) < lenpos: currposptr +=1
            else:break
        negptr += 1
        numloops +=1
        if numloops%10000 == 0: print(int(numloops *100 / len(neglist)),"percent completed")
    return target




if __name__ == "__main__":
    import time
    timestart = time.time()
    from openfile import openNumberstoListfromFile
    from openfile import writelisttofile
    # inputList = openNumberstoListfromFile("data/million_numbers.txt")
    # inputList = list(set(inputList ))
    # quickSort(inputList)
    # writelisttofile("data/sortedmillion_numbers.txt",inputList)
    inputList = openNumberstoListfromFile("data/sortedmillion_numbers.txt")
    posnum = [i for i in inputList if i >= 0][::-1]
    negnum = [i for i in inputList if i < 0]
    lenpos = len(posnum)
    lenneg = len(negnum)
    timefunc= time.time()
    print(len(sum2betweenwith2lists(posnum,negnum,10000,-10000,lenpos,lenneg)))
    print("time taken = ",time.time()-timefunc)
    print("total time taken = ",time.time()-timestart)

    # timestart - time.time()
    # betweentuples = sumTwoBetweenwithPosNegLists(posnum,negnum,10000,-10000)
    # print(betweentuples[:10])
    # res = set()
    # for elem in betweentuples:
    #     res.add(elem[0])
    # #print(res)
    # print("length of res = ",len(res))
    # print("time taken = ",time.time() - timestart)
    # writelisttofile("data/sortedmillion_numberspositive.txt",list(posnum))
    # writelisttofile("data/sortedmillion_numbersnegative.txt",list(negnum))

