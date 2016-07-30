# Multiplying matrices
# Ideal speed is when matrix is square in size 2^n


#define addition of matrices
def addm(m1,m2):
    #assuming m1 and m2 of same size
    z=[]
    for i in range(len(m1)):
        row=[]
        for j in range(len(m1[0])):
            row.append(m1[i][j] + m2[i][j])
        z.append(row)
    return z
# define scalar matrix multiplication
def scalarmult(m1,c):
    z=[]
    for i in range(len(m1)):
        row=[]
        for j in range(len(m1[0])):
            row.append(c*m1[i][j])
        z.append(row)
    return z

#define subsetting of matrices
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


#define the algorithm itself
def mmult(m1,m2):
    if len(m1) == 1 and len(m1[0]) == 1 and len(m2)==1 and len(m2[0]) ==1:
        return [[m1[0][0]*m2[0][0]]]
    elif len(m1) == 1 and len(m1[0]) == 1:
        return scalarmult(m2,m1[0][0])
    elif len(m2) == 1 and len(m2[0]) == 1:
        return scalarmult(m1,m2[0][0])

    padded = False
    if len(m1)%2 ==1:
        padded=True
        m1.append([0 for i in range(len(m1[0]))])
        m2.append([0 for i in range(len(m1[0]))])
        for i in range(len(m1)):
            m1[i].append(0)
            m2[i].append(0)
    k = int(len(m1)/2)
    A = subsetm(m1,range(0,k),range(0,k))
    B = subsetm(m1,range(0,k),range(k,len(m1[1])))
    C = subsetm(m1,range(k,len(m1)),range(0,k))
    D = subsetm(m1,range(k,len(m1)),range(k,len(m1[1])))
    E = subsetm(m2,range(0,k),range(0,k))
    F = subsetm(m2,range(0,k),range(k,len(m2[1])))
    G = subsetm(m2,range(k,len(m2)),range(0,k))
    H = subsetm(m2,range(k,len(m2)),range(k,len(m2[1])))
    #print("A = ",A,"\nB = ",B,"\nC = ",C,"\nD = ",D,"\nE = ",E,"\nF = ",F,"\nG = ",G,"\nH = ",H)
    FH = addm(F,scalarmult(H,-1))
    AB = addm(A,B)
    CD = addm(C,D)
    GE = addm(G,scalarmult(E,-1))
    AD = addm(A,D)
    EH = addm(E,H)
    BD = addm(B,scalarmult(D,-1))
    GH = addm(G,H)
    AC = addm(A,scalarmult(C,-1))
    EF = addm(E,F)

    P1 = mmult(A,FH)
    P2 = mmult(AB,H)
    P3 = mmult(CD,E)
    P4 = mmult(D,GE)
    P5 = mmult(AD,EH)
    P6 = mmult(BD,GH)
    P7 = mmult(AC,EF)

    Topleft = addm(addm(addm(P5,P4),scalarmult(P2,-1)),P6)
    Topright = addm(P1,P2)
    Botleft = addm(P3,P4)
    Botright = addm(addm(addm(P1,P5),scalarmult(P3,-1)),scalarmult(P7,-1))
    #print("TL = ",Topleft,"\nTR = ",Topright,"\nBL = ",Botleft,"\nBR = ",Botright)
    res = [[0 for i in range(len(Topleft[0])+ len(Topright[0]))] for j in range(len(Topleft) + len(Botleft))]
    i = 0
    j = 0
    for i in range(len(Topleft[0])):
        for j in range(len(Topleft)):
            res[i][j] = Topleft[i][j]
    i = 0
    j = 0
    for i in range(len(Topright[0])):
        for j in range(len(Topright)):
            res[i][j+len(Topleft[0])] = Topright[i][j]
    i = 0
    j = 0
    for i in range(len(Botleft[0])):
        for j in range(len(Botleft)):
            res[i+len(Topleft)][j] = Botleft[i][j]
    i = 0
    j = 0
    for i in range(len(Botright[0])):
        for j in range(len(Botright)):
            res[i+len(Topleft)][j+len(Topleft[0])] = Botright[i][j]
    #print(res,padded)
    if padded == False: return res
    if padded == True: return subsetm(res,range(len(res)-1),range(len(res[0])-1))

def column(matrix, i):
    return [row[i] for row in matrix]




#Do some checks
'''
A = [[1,2,3,4], [5,6,7,8],[9,10,11,12],[13,14,15,16]]
B = [[111,112,113,114], [115,116,117,118],[119,1110,1111,1112],[1113,1114,1115,1116]]
print(mmult(A,B))

A = [[1,2,3],[4,5,6],[7,8,9]]
B = [[10,11,12],[13,14,15],[16,17,18]]
print(mmult(A,B))


'''



'''
A = [[1]]
B = [[3]]
print("A = " , A," B = ",B," addition leads to ",addm(A,B))

A = [[2,4,1], [7,0,2]]
B = [[3,1,1], [-1,8,5]]
print("A = " , A," B = ",B," addition leads to ",addm(A,B))
A = [[2,4,4], [7,0,3]]
B = [[3,1,1], [-1,8,5]]
print("A = " , A," B = ",B," addition leads to ",addm(A,B))

a = [[2,4,6,7,5], [7,0,8,3,5], [6,3,2,1,5],[1,2,3,4,5]]
k = int(len(a)/2)
print("A = " , a,"\nk = ",k, "\nSubset from row range = k to 2k and col range = k to 2k+1 = \n", subsetm(a,range(k,2*k),range(k,2*k+1)))

a = [[2]]
k = int(len(a)/2)
print("A = " , a,"\nk = ",k, "\nSubset from row range = k to 2k and col range = k to 2k+1 = \n", subsetm(a,range(k,2*k),range(k,2*k+1)))
'''
