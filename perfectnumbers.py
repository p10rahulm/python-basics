
# program finds n perfect numbers
from findfactors import factors
from math import sqrt

def findperfectnumbers(n):
    ans = []
    numperfect=0
    iter = 0
    while numperfect < n:
        if iter%10000==0:print(iter)
        if checksumfactorsis2n(iter):
            #the 2*iter is because the function returns the factors including the number itself
            if int(sqrt(iter))**2 != iter:
                numperfect +=1
                ans.append(iter)
        iter +=1
    return ans

def checksumfactorsis2n(n):
    step = 2 if n%2 else 1
    sum =0
    sqrtn= int(sqrt(n))+1
    i=1
    while i< sqrtn and sum<2*n:
        if n % i == 0:
            sum+= i + n//i
        i+=step
    return sum==2*n



if __name__ == "__main__":
    # The algorithm works great till 5 perfect numbers (8128 being the last), but fails on the 6th which is 33550336
    print(findperfectnumbers(4))
    print(checksumfactorsis2n(33550336))
    #Need to find a better method to eliminate



