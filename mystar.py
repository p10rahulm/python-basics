from math import sqrt
def createstar(size = 60):
    m = [[i for i in range(size)]for i in range(size)]

    res = [[0 for i in range(size)] for j in range(size)]
    res = drawhorizontals(res,size)
    res = forw1(res,size)
    res = back1(res,size)
    res = forw2(res,size)
    res = back2(res,size)
    import re
    for i in range(size):
        print(re.sub("[\']","",re.sub("[0\,\[\]]"," ",str(res[i]))))

def drawhorizontals(res,size):
    p = res.copy()
    for i in range(size):
        p[int((size-1) - (size/2*sqrt(3)))][i] = "*"
        p[int(size/2*sqrt(3))][i] = "*"
    return p
def forw1(res,size):
    p = res.copy()
    for i in range(int(size/2*sqrt(3))+1):
        p[int(size/2*sqrt(3))-i][int(i/sqrt(3))] = "*"
    return p

def back1(res,size):
    p = res.copy()
    for i in range(int(size/2*sqrt(3))+1):
        p[int(size/2*sqrt(3))-i][(size - 1) - int(i/sqrt(3))] = "*"
    return p

def forw2(res,size):
    p = res.copy()
    for i in range(int(size/2*sqrt(3))+1):
        p[int((size-1) - (size/2*sqrt(3)))+i][int(i/sqrt(3))] = "*"
    return p

def back2(res,size):
    p = res.copy()
    for i in range(int(size/2*sqrt(3))+1):
        p[int((size-1) - (size/2*sqrt(3)))+i][(size - 1) - int(i/sqrt(3))] = "*"
    return p

if __name__ == "__main__":
    createstar(25)