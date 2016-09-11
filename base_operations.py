import time

hexnames = dict((i,hex(1)[2:])for i in range(16))

def dectohex(number):
    outstring = ''
    while number > 0:
        outstring += hexnames[number%16]
        number //=16
    return outstring
def findmin(arr):
    minsofar=1000000
    maxdiffsofar = 0
    for i in range(len(arr)):
        if arr[i] < minsofar:
            minsofar = arr[i]
        if arr[i] - minsofar >maxdiffsofar:
            maxdiffsofar = arr[i] - minsofar

    if maxdiffsofar ==0:        return -1
    return maxdiffsofar

def findcubes(m,n):
    i = 0
    print("m=",m)
    while i**3 <=m:
        i+=1
        print("i=",i)
    j =0
    print("n=",n)
    while j**3 <=n:
        j+=1
        print("j=",j)
    return (i-1)*(j-1)




def is_perfect_cube(n):
    c = int(n**(1/3.))
    return (c**3 == n) or ((c+1)**3 == n)

if __name__ == "__main__":
    timestart = time.time()
    for j in range(1000):
        for i in range(1000):
            dectohex(i)
    print("time taken = ",time.time()-timestart)
