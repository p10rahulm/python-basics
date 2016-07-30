def subsetm(listOfLists,rangerow,rangecol):
    "Flatten one level of nesting"
    res = [[0 for i in range(len(rangecol))] for j in range(len(rangerow))]

    # Debugging
    #print("list of lists = ",listOfLists,"\nrangerows = ",rangerow,"rangecols = ",rangecol)
    #print("res = ",res)
    rowm = 0
    colm = 0
    for i in (rangerow):
        for j in (rangecol):
            res[rowm][colm] = listOfLists[i][j]
            colm+=1
        rowm+=1
        colm = 0
    return res

def column(matrix, i):
    return [row[i] for row in matrix]


