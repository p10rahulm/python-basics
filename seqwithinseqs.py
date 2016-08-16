# This is the driver function which takes in a) the search sequences and replacements as a dictionary and b) the full sequence in which to search as a list
def findSeqswithinSeq(searchSequences,baseSequence):
    seqkeys = [[int(i) for i in elem.split(",")] for elem in searchSequences]
    maxlen = max([len(elem) for elem in seqkeys])
    decisiontree = getdecisiontree(seqkeys)
    i = 0
    while i < len(baseSequence):
        (increment,replacement) = get_increment_replacement(decisiontree,baseSequence[i:i+maxlen])
        if replacement != -1:
            baseSequence[i:i+len(replacement)] = searchSequences[",".join(map(str,replacement))]
        i +=increment
    return  baseSequence

#the following function gives the dictionary of intermediate sequences allowed
def getdecisiontree(searchsequences):
    dtree = {}
    for elem in searchsequences:
        for i in range(len(elem)):
            if i+1 == len(elem):
                dtree[",".join(map(str,elem[:i+1]))] = True
            else:
                dtree[",".join(map(str,elem[:i+1]))] = False
    return dtree

#the following is the function does most of the work giving us a) how many positions we can skip in the search and b)whether the search seq was found
def get_increment_replacement(decisiontree,sequence):
    if str(sequence[0]) not in decisiontree:
        return (1,-1)
    for i in range(1,len(sequence)):
        key = ",".join(map(str,sequence[:i+1]))
        if key not in decisiontree:
            return (1,-1)
        elif decisiontree[key] == True:
            key = [int(i) for i in key.split(",")]
            return (len(key),key)
    return 1, -1



#The following code can test whether the above works
if __name__ == "__main__":
    inputlist = [5,4,0,1,1,1,0,2,0,1,0,99,15,1,0,1]
    patternsandrepls = {'0,1,0':[0,0,0],
                        '0,1,1,0':[0,0,0,0],
                        '0,1,1,1,0':[0,0,0,0,0],
                        '1,0,1':[1,1,1],
                        '1,0,0,1':[1,1,1,1],
                        '1,0,0,0,1':[1,1,1,1,1]}

    print(findSeqswithinSeq(patternsandrepls,inputlist))
