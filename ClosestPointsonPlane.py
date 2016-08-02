from Mergesort import mergesorts
from Mergesort import mergesorttwolists
from AvgMedian import nth_element_in_list

#check distance between points
#input x and y coords
def distance(xc1,yc1,xc2,yc2):
    return ((xc1-xc2)**2 + (yc1-yc2)**2)**0.5


def closest(xcoords,ycoords):
    if len(xcoords) ==2:
        return [xcoords[0],ycoords[0],xcoords[1],ycoords[1],distance(xcoords[0],ycoords[0],xcoords[1],ycoords[1])]
    subysorted, subxsorted = mergesorttwolists(ycoords,xcoords)
    ycoords = subysorted
    xcoords = subxsorted

    k = int(len(xcoords)/2)
    leftx = xcoords[:k]
    lefty = ycoords[:k]
    rightx = xcoords[k:]
    righty = ycoords[k:]

    bestleft = closest(leftx,lefty)
    bestright = closest(rightx,righty)
    delta = min(bestleft[4],bestright[4])
    #print("bestleft is\n",bestleft)
    #print("bestright is\n",bestright)
    #print("xcoords and ycoords are \n",xcoords,"\n",ycoords)
    bestsplit = closestsplitpair(xcoords,ycoords,delta)
    #print("bestsplit is\n",bestsplit)
    bestd = min(bestleft[4],bestright[4],bestsplit[4])
    if bestleft[4] == bestd:
        return bestleft
    elif bestright[4] == bestd:
        return bestright
    elif bestsplit[4] == bestd:
        return bestsplit

def closestsplitpair(xcoords,ycoords,delta):
    sorted_x = mergesorts(xcoords)
    xbar = sorted_x[int(len(xcoords)/2)]
    xbar = nth_element_in_list(xcoords, int(len(xcoords)/2))
    #print("xbar is ",xbar,"delta is ",delta)
    minx = xbar - delta
    maxx = xbar + delta
    subx = []
    suby = []
    for i in range(len(xcoords)):
        if xcoords[i] >=minx and xcoords[i]<= maxx:
            subx.append(xcoords[i])
            suby.append(ycoords[i])
    #print("subx = ",subx,"suby = ",suby)
    bestd = [None,None,None,None,delta]

    for i in range(len(suby)-1):
        for j in range(min(7,len(suby)-i-1)):
            if distance(subx[i],suby[i],subx[i+j+1],suby[i+j+1]) < bestd[4]:
                #print("Now bettering the best")
                bestd[4] = distance(subx[i],suby[i],subx[i+j+1],suby[i+j+1])
                #print("bestd[4] set as", bestd[4])
                bestd[0] = subx[i]
                bestd[1] = suby[i]
                bestd[2] = subx[i+j+1]
                bestd[3] = suby[i+j+1]
    return bestd

def convert_list_of_tuples_to_list_of_coords(listAll):
    xcoords = []
    ycoords = []
    for i in range(len(listAll)):
        xcoords.append(listAll[i][0])
        ycoords.append(listAll[i][1])
    return xcoords,ycoords


if __name__ == "__main__":
    ###Tests----------------------------
    xcoords = [0,1,0,0]
    ycoords = [-5,5,25,85]
    print("X Coordinates of points are",xcoords,"\nY Coordinates of points are",ycoords,
          "\nshortest distances are between points and distance is: ",closest(xcoords,ycoords))

    A = [(0,-5),(1,5),(0,25),(0,85)]
    xcoords,ycoords = convert_list_of_tuples_to_list_of_coords(A)
    print("X Coordinates of points are",xcoords,"\nY Coordinates of points are",ycoords,
          "\nshortest distances are between points and distance is: ",closest(xcoords,ycoords))

    A = [8,4,1,6,7,2,6,2,2221]
    print(mergesorts(A))
    A = [1,2,3,4,5,6,7,8,10,9]
    B = [10,9,8,7,6,5,4,3,2,1]
    print("A = \n" , A , "\nB = ",B,"\nMerged and sorted lists are\n" , mergesorttwolists(A,B))
