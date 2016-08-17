from itertools import permutations
from math import sqrt

def check_magic_square(rangeallowed,sumMS):
    sidelenght = int(sqrt(len(rangeallowed)))
    for i in permutations(rangeallowed):
        MSConditionsSatisfied = True
        if (MSConditionsSatisfied and sum(i[::sidelenght+1]) != sumMS): MSConditionsSatisfied = False
        if (MSConditionsSatisfied and sum(i[sidelenght-1:-1:sidelenght-1]) != sumMS): MSConditionsSatisfied = False
        for j in range(sidelenght):
            if (MSConditionsSatisfied and sum(i[j::sidelenght]) != sumMS): MSConditionsSatisfied = False
            if (MSConditionsSatisfied and sum(i[j*sidelenght:(j+1)*sidelenght]) != sumMS): MSConditionsSatisfied = False
        if MSConditionsSatisfied: return [[i[k*sidelenght + j] for j in range(sidelenght)] for k in range(sidelenght)]
    return False

if __name__ == "__main__":
    import time
    starttime  = time.time()
    print(check_magic_square(range(1,10),15))
    print("time taken =",time.time()-starttime)