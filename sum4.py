import sys
import itertools
from PIL import Image
import random
def sum4equals(arr,sumno):
    nummax = max(arr)
    p = []
    for i in range(1,nummax-2):
        for j in range(i+1,nummax-1):
            for k in range(j+1,nummax):
                for l in range(k+1,nummax):
                    if i +j+k+l ==sumno:
                        p.append((i,j,k,l))
    return p

def permute(lista):
    returnlist = []
    for val in lista:
        val2 = list(val)
        for i in itertools.permutations(val2):
            returnlist.append(i)
    return returnlist



def create_image(imlist):
    # 1_Triangle-04
    picspath = dict((s, "data/img/"+s+ "/1_"+ s +"-0")
             for s in imlist)
    # print(picspath)
    #opens an image:
    im = Image.open("data/img/Circle/1_Circle-01.png")


    #creates a new empty image, RGB mode, and size 400 by 400.
    new_im = Image.new('RGB', (400,400),"white")
    #Here I resize my opened image, so it is no bigger than 100,100
    im.thumbnail((100,100))
    #Iterate through a 4 by 4 grid with 100 spacing, to place my image
    for i in range(0,400,100):
        for j in range(0,400,100):
            #I change brightness of the images, just to emphasise they are unique copies.


            indx=int(4*i/100+j/100)
            img=Image.open(picspath[imlist[indx]]+str(random.randint(1,9))+".png")
            # print("indx=",indx,"i=",i,"j=",j)
            im=Image.eval(img,lambda x: x+(i+j)/30)
            # im.thumbnail((100,100))
            # paste the image at location i,j:
            new_im.paste(im, (i,j))
    return new_im

def createimages(permutedlist4s,imageslist):
    i = random.randint(0,len(permutedlist4s))
    p = []
    for j in range(len(imageslist)):
        p += [imageslist[j]] * permutedlist4s[i][j]
    random.shuffle(p)
    return create_image(p)





if __name__ == "__main__":
    arr = list(range(1,11))
    list4s  = sum4equals(arr,16)
    permutedlist4s = permute(list4s)
    imlist = ["Circle","Square","Rectangle","Triangle"]
    for i in range(200):
        result = createimages(permutedlist4s,imlist)
        result.save("data/img/Output1616/out"+str(i)+".bmp")



