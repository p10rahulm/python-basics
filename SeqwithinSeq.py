#from collections import defaultdict

def findSeqswithinSeq(searchSequences,baseSequence):
    seqkeys = [[int(i) for i in elem.split(",")] for elem in searchSequences]
    maxlen = max([len(elem) for elem in seqkeys])
    decisiontree = getdecisiontree(seqkeys)
    print("seqkeys=",seqkeys,"\ndecisiontree=\n",decisiontree,"\nmaxlen = ",maxlen)
    i = 0
    while i < len(baseSequence):
        (increment,replacement) = get_increment_replacement(decisiontree,baseSequence[i:i+maxlen])
        print("(increment,replacement)  = ",(increment,replacement))
        doreplacement(searchSequences,baseSequence,i,replacement)
        i +=increment
    return  baseSequence

def getdecisiontree(searchsequences):
    #dtree = defaultdict(list)
    dtree = {}
    for elem in searchsequences:
        for i in range(len(elem)):
            if i+1 == len(elem):
                dtree[",".join(map(str,elem[:i+1]))] = True
            else:
                dtree[",".join(map(str,elem[:i+1]))] = False
            #elif elem[:i+2] not in dtree[",".join(map(str,elem[:i+1]))]:
            #    dtree[",".join(map(str,elem[:i+1]))].append(elem[:i+2])
    return dtree





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




def doreplacement(searchSequences,baseSequence,i,replacement):
    if replacement == -1:
        return
    else:
        baseSequence[i:i+len(replacement)] = searchSequences[",".join(map(str,replacement))]
        return



if __name__ == "__main__":
    inputlist = [5,4,0,1,1,1,0,2,0,1,0,99,15,1,0,1]
    #patternsandrepls = {[0,1,0]:[0,0,0],[0,1,1,0]:[0,0,0,0],[0,1,1,1,0]:[0,0,0,0,0],[1,0,1]:[1,1,1],[1,0,0,1]:[1,1,1,1],[1,0,0,0,1]:[1,1,1,1,1]}
    patternsandrepls = {'0,1,0':[0,0,0],
                        '0,1,1,0':[0,0,0,0],
                        '0,1,1,1,0':[0,0,0,0,0],
                        '1,0,1':[1,1,1],
                        '1,0,0,1':[1,1,1,1],
                        '1,0,0,0,1':[1,1,1,1,1]}

    print(findSeqswithinSeq(patternsandrepls,inputlist))
