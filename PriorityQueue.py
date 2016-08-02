# See http://en.wikipedia.org/wiki/Priority_queue
# You should choose binary or fibonacci heap, based on how you plan to use it:
#
# O(log(N)) insertion time and O(1) findMin+deleteMin time - bin search heap, or
# O(1) insertion time and O(log(N)) findMin+deleteMin time
# In the latter case, you can choose to implement a priority queue with a Fibonacci heap:
# http://en.wikipedia.org/wiki/Heap_(data_structure)#Comparison_of_theoretic_bounds_for_variants
# (as you can see, heapq which is basically a binary tree, must necessarily have O(log(N)) for both
# insertion and findMin+deleteMin)
#
# From: https://github.com/danielborowski/fibonacci-heap-python
# They are complicated when it comes to coding them. Also they are not as efficient in practice when 
# compared with the theoretically less efficient forms of heaps, since in their simplest version they require 
# storage and manipulation of four pointers per node, compared to the two or three pointers per node needed 
# for other structures
# We therefore code the priority queue as a binary heap and added the fibonacci heap as a separate structure
#
# Operation	    Binary[1]	Binomial[1]	Fibonacci[1]	Pairing[2]	Brodal[3][a]	Rank-pairing[5]	Strict Fibonacci[6]
# find-min	    Θ(1)	    Θ(1)	    Θ(1)	        Θ(1)	    Θ(1)	        Θ(1)	        Θ(1)
# delete-min	Θ(log n)	Θ(log n)	O(log n)[b]	    O(log n)	O(log n)	    O(log n)[b]	    O(log n)
# insert	    Θ(log n)	Θ(1)	    Θ(1)	        Θ(1)	    Θ(1)	        Θ(1)	        Θ(1)
# decrease-key	Θ(log n)	Θ(log n)	Θ(1)	        o(log n)	Θ(1)	        Θ(1)[b]	        Θ(1)
# merge	        Θ(n)	    O(log n)	Θ(1)	        Θ(1)	    Θ(1)	        Θ(1)	        Θ(1)


import time
class PriorityQueue(object):
    def __init__(self,inputArray=None):
        if inputArray == None:
            self.heapList = []
            self.currentSize = 0
        else:
            self.heapList = inputArray
            self.buildHeap(self.heapList)
            self.currentSize = len(inputArray)

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

    def extractMin(self):
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

    def empty(self):
        if self.currentSize == 0: return True
        else: return False

    def show(self):
        print(self.heapList)

    def __str__(self):
        return str(self.heapList)


if __name__ == "__main__":
    # test 1
    print("test 1")
    timestart = time.time()
    for i in range(100000):
        p = PriorityQueue()
        p.insert(10)
        p.insert(5)
        p.insert(2)
        p.insert(100)
        p.insert(1)
        p.insert(12)

    print(p)
    print("time taken = ",time.time()-timestart)

    # test 2
    print("test 2")
    timestart = time.time()
    for i in range(100000):
        p = PriorityQueue()
        p.insert((10,"hi10"))
        p.insert((5,"hi5"))
        p.insert((2,"yo"))
        p.insert((100,"tendulkar"))
        p.insert((1,"uno"))
        p.insert((12,"dozen"))

    print(p)
    print("time taken = ",time.time()-timestart)



