# You are a given a unimodal array of n distinct elements,
# meaning that its entries are in increasing order up until
# its maximum element, after which its elements are in decreasing
# order. Give an algorithm to compute the maximum element that runs
# in O(log n) time.

def unimodalmax(listA):
    # create left half and right half, if
    # left half last element < right half first element
    # continue looking in right half,
    # else, look in left half
    # Add base case

    if len(listA) == 2:
        return max(listA[1],listA[0])
    if len(listA) == 1:
        return listA[0]

    k = int(len(listA)/2)
    L = listA[0:k]
    R = listA[k:]
    if L[-1] < R[0]:
        return unimodalmax(R)
    else: return unimodalmax(L)
if __name__ == "__main__":
    print(unimodalmax([1,2,3,4,3,2,1]))