def secondhighest(listA):
    best = listA[1]
    secbest = listA[1]
    for i in range(len(listA)):
        if listA[i]>secbest:
            if listA[i] > best:
                secbest = best
                best = listA[i]
            else:
                secbest = listA[i]
    return secbest

if __name__ == "__main__":
    A = [1,2,3,1,2,5,6,6]
    print("second highest in array A = ",A, "is ",secondhighest(A))
