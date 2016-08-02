import time
class minHeap(object):
    def __init__(self,heaplist_input=None):
        if heaplist_input == None:
            self.heapList = []
            self.currentSize = 0
        else:
            self.heapList = heaplist_input
            self.buildHeap(self.heapList)
            self.currentSize = len(heaplist_input)

    def percUp(self,node_index):
        while (node_index - 1)//2 >= 0:
            if self.heapList[node_index] < self.heapList[(node_index - 1)//2]:
                self.__swap(node_index,(node_index - 1)//2)
            node_index = (node_index - 1)//2

    def __swap(self,firstindex,secondindex):
         tmp = self.heapList[secondindex]
         self.heapList[secondindex] = self.heapList[firstindex]
         self.heapList[firstindex] = tmp

    def insert(self,insertElement):
        self.heapList.append(insertElement)
        self.currentSize = self.currentSize + 1
        self.percUp(self.currentSize-1)

    def percDown(self,node_index):
        while (node_index*2 + 1) < self.currentSize:
            minchild = self.minchild(node_index)
            if self.heapList[node_index] > self.heapList[minchild]:
                self.__swap(node_index,minchild)
            node_index = minchild

    def minchild(self,node_index):
        if (node_index + 1)*2 >= self.currentSize:
            return node_index*2 + 1
        else:
            if self.heapList[node_index*2 + 1] < self.heapList[(node_index + 1)*2]:
                return node_index*2 + 1
            else:
                return (node_index + 1)*2

    def delmin(self):
        min = self.heapList[0]
        self.heapList[0] = self.heapList[self.currentSize-1]
        self.currentSize = self.currentSize - 1
        self.heapList.pop()
        self.percDown(0)
        return min

    def buildHeap(self,input_list):
        itercounter = len(input_list) // 2
        self.currentSize = len(input_list)
        self.heapList = input_list[:]
        while (itercounter >= 0):
            self.percDown(itercounter)
            itercounter = itercounter - 1

    def show(self):
        print(self.heapList)

    def __str__(self):
        return str(self.heapList)


if __name__ == "__main__":
    #test 1
    print("test 1")
    timestart = time.time()
    for i in range(100000):
        p = minHeap()
        p.insert(10)
        p.insert(5)
        p.insert(2)
        p.insert(100)
        p.insert(1)
        p.insert(12)

    print(p)
    print("time taken = ",time.time()-timestart)

    #test 2
    print("test 2")
    timestart = time.time()
    for i in range(100000):
        p = minHeap()
        p.insert((10,"hi10"))
        p.insert((5,"hi5"))
        p.insert((2,"yo"))
        p.insert((100,"tendulkar"))
        p.insert((1,"uno"))
        p.insert((12,"dozen"))

    print(p)
    print("time taken = ",time.time()-timestart)
