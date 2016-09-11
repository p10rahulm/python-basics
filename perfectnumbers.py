
# program finds n perfect numbers
from findfactors import factors

def findperfectnumbers(n):
    ans = []
    numperfect=0
    iter = 0
    while numperfect < n:
        if sum(factors(iter)) == iter:
            numperfect +=1
            ans.append(iter)
        iter +=1

if __name__ == "__main__":
    print(findperfectnumbers(3))



