# We are going to implement this using Heaps. The median is stored in the root with a min heap as the
# right child and a max heap as the left child of the root node.
from minHeap import minHeap
from maxHeap import maxHeap
class Root(object):
    def __init__(self,value = None):
        self.leftchild = None
        self.rightchild = None
        self.value = value



class minmaxHeap(object):
    def __init__(self):
        self.root = Root()
        self.minheap = minHeap()
        self.maxheap = maxHeap()
        self.root.leftchild = self.maxheap
        self.root.rightchild = self.minheap
        self.balance = 0

    def insert(self,insertElement):
        if self.root.value is None:
            self.root.value = insertElement
            self.balance = 0
            return self.root.value
        if insertElement >= self.root.value:
            self.minheap.insert(insertElement)
            self.balance +=1
        elif insertElement < self.root.value:
            self.maxheap.insert(insertElement)
            self.balance -=1
        else: raise("please check inserted element")
        self.rebalance()
        return self.root.value

    def rebalance(self):
        while self.balance > 1 or self.balance < 0 :
            if self.balance < 0:
                maxheapmax = self.maxheap.delmax()
                temproot = self.root.value
                self.root.value = maxheapmax
                self.minheap.insert(temproot)
                self.balance +=2
            elif self.balance > 1:
                minheapmin = self.minheap.delmin()
                temproot = self.root.value
                self.root.value = minheapmin
                self.maxheap.insert(temproot)
                self.balance -=2




if __name__ == "__main__":
    import time
    timestart = time.time()
    print("test1")
    xlist = [1,2,3]
    medianslist = []
    medianHeap = minmaxHeap()
    for i in range(len(xlist)): #element in xlist:
        mediannow = medianHeap.insert(xlist[i])
        medianslist.append(mediannow)
        print(medianslist)


    timestart = time.time()
    print("test 2")
    from openfile import openfile_returnlist
    xlist = openfile_returnlist("data/medianmaint.txt")
    medianslist = []
    medianHeap = minmaxHeap()
    for i in range(len(xlist)): #element in xlist:
        mediannow = medianHeap.insert(xlist[i])
        medianslist.append(mediannow)
        #if i%100 ==0: print(i/100,"percent complete")
    from openfile import writelisttofile
    writelisttofile("data/medianslist.txt",medianslist)
    print("sum = ",sum(medianslist))
    print("sum %10000 = ",sum(medianslist)%10000)
    print("time taken = ",time.time()-timestart)