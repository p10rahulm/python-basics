import time

hexnames = dict((i,hex(1)[2:])for i in range(16))

def dectohex(number):
    outstring = ''
    while number > 0:
        outstring += hexnames[number%16]
        number //=16
    return outstring


if __name__ == "__main__":
    timestart = time.time()
    for j in range(1000):
        for i in range(1000):
            dectohex(i)
    print("time taken = ",time.time()-timestart)
