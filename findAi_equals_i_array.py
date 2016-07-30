#STRICTLY INCREASING

def find_ai_equals_i(listA,indexstart):
    # You are given a sorted (from smallest to largest) array A of n distinct integers which
    # can be positive, negative, or zero. You want to decide whether or not there is an index i
    # such that A[i] = i. Design the fastest algorithm that you can for solving this problem.
    if len(listA) == 1:
        if (listA[0]) == indexstart +1: return True
        else: return False
    k = int(len(listA)/2)
    L = listA[:k]
    R = listA[k:]
    if R[0]== k+1 + indexstart:
        return True
    else:
        RT = find_ai_equals_i(R,k+indexstart)
        LT = find_ai_equals_i(L,indexstart)
        return RT or LT

#Do some checks
A = [-5,-1,3,11]
print("A = ",A,"Does Ai have A[i] = i ? ", find_ai_equals_i(A,0))
A = [-5,-1,1,4]
print("A = ",A,"Does Ai have A[i] = i ? ", find_ai_equals_i(A,0))
A = [-5,-1,3,15,16]
print("A = ",A,"Does Ai have A[i] = i ? ", find_ai_equals_i(A,0))
A = [-5,2,5,15,16]
print("A = ",A,"Does Ai have A[i] = i ? ", find_ai_equals_i(A,0))
A = [-5,-1,1,11]
print("A = ",A,"Does Ai have A[i] = i ? ", find_ai_equals_i(A,0))
'''
A = [-5,-1,1,7]
print("A = ",A,"Does Ai have A[i] = i ? ", find_ai_equals_i(A,0))
'''
A = [-5,-1,0,15,16]
print("A = ",A,"Does Ai have A[i] = i ? ", find_ai_equals_i(A,0))
A = [-5,1,5,15,16]
print("A = ",A,"Does Ai have A[i] = i ? ", find_ai_equals_i(A,0))
A = [0,0,0,0]
print("A = ",A,"Does Ai have A[i] = i ? ", find_ai_equals_i(A,0))
A = [1,1,1,1]
print("A = ",A,"Does Ai have A[i] = i ? ", find_ai_equals_i(A,0))
