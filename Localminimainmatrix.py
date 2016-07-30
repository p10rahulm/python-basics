from matrixmult import column
from matrixmult import subsetm
def findlocalminima(matrixA):
    #print(matrixA)
    if len(matrixA) == 1 or len(matrixA[0]) ==1:
        return min(matrixA)
    rows = len(matrixA)
    cols = len(matrixA[0])
    midrow = int(rows/2)
    midcol = int(cols/2)
    fullset = column(matrixA,0)+column(matrixA,midcol) + column(matrixA,cols-1)\
              + matrixA[0] + matrixA[midrow] + matrixA[-1]

    indexofmin = fullset.index(min(fullset))
    if int(indexofmin/(3*cols)) == 0: position = int(indexofmin/(3*cols))+int(indexofmin/cols)
    else: position = 3 + int((indexofmin-3*cols)/rows)
    #print("fullset = ",fullset,"index of minimum = ",indexofmin,"position = ",position)

    if position == 0 or position == 1 or position == 2 :
        rowmin = indexofmin%rows
        if position == 0: colmin = 0
        elif position == 1: colmin = midcol
        elif position == 2: colmin = cols - 1
    elif position == 3 or position == 4 or position == 5 :
        colmin = indexofmin%cols
        if position == 3: rowmin = 0
        elif position == 4: rowmin = midrow
        elif position == 5: rowmin = rows - 1
    chkleft = True if colmin != 0 else False
    chkright = True if colmin != cols-1 else False
    chktop  = True if rowmin != 0 else False
    chkbot  = True if rowmin != rows-1 else False
    leftlower = False;rightlower=False;toplower=False;botlower=False
    if chkleft:
        if matrixA[rowmin][colmin-1] < matrixA[rowmin][colmin]:
            leftlower = True
    if chkright:
        if matrixA[rowmin][colmin+1] < matrixA[rowmin][colmin]:
            rightlower = True
    if chktop:
        if matrixA[rowmin-1][colmin] < matrixA[rowmin][colmin]:
            toplower = True
    if chkbot:
        if matrixA[rowmin+1][colmin] < matrixA[rowmin][colmin]:
            botlower = True

    if leftlower == False and rightlower==False and toplower==False and botlower==False:
        return matrixA[rowmin][colmin]
    subcolsize = int((cols-3)/2 + 0.5)
    subrowsize = int((rows-3)/2 + 0.5)

    if rightlower:
        A = subsetm(matrixA,range(int(rowmin/midrow)+1,int(rowmin/midrow) + subrowsize+1),range(colmin+1,colmin+subcolsize+1))
        return findlocalminima(A)
    elif leftlower:
        A = subsetm(matrixA,range(int(rowmin/midrow)+1,int(rowmin/midrow) + subrowsize+1),range(colmin-subcolsize,colmin))
        return findlocalminima(A)
    elif botlower:
        A = subsetm(matrixA,range(rowmin+1,rowmin + subrowsize+1),range(int(colmin/midcol)+1,int(colmin/midcol)+subcolsize+1))
        return findlocalminima(A)
    elif toplower:
        A = subsetm(matrixA,range(rowmin-subrowsize,rowmin),range(int(colmin/midcol)+1,int(colmin/midcol)+subcolsize+1))
        return findlocalminima(A)

A = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
print("A = ",A,"\nLocal minima is ", findlocalminima(A))
A = [[11, 10, 12,14], [3,0, 4, 5], [6,15,7, 8], [1,12,12, 8]]
print("A = ",A,"\nLocal minima is ", findlocalminima(A))
A = [[66,   14,   13   ,86   ,19   ,96   ,65   ,49   ,41   ,55],
 [10   ,82   ,84   ,99   ,16   ,52   ,73   ,11   ,18   ,29],
 [90   ,68   ,60    ,7   ,95  ,100   ,37   ,21   ,34   ,93],
 [97   ,75   ,63   ,69   ,26   ,56   ,22   ,67    ,6   ,42],
 [38   ,32   ,71   ,61   ,48   ,76   ,91   ,17   ,53   ,40],
 [87   ,74   ,80   ,64   ,25    ,9   ,28   ,31   ,36    ,5],
 [79   ,72   ,92   ,83   ,59   ,85    ,8   ,39   ,70   ,27],
 [77   ,50   ,89   ,44   ,47   ,12   ,2   ,30   ,45   ,24],
 [46   ,94    ,1   ,35   ,58   ,20    ,4   ,51   ,15   ,98],
 [54   ,57    ,3   ,43   ,88   ,23    ,81   ,78   ,33   ,62]]
print("A = ",A,"\nLocal minima is ", findlocalminima(A))
