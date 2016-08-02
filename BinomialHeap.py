# http://www.geeksforgeeks.org/binomial-heap-2/
# Operation	    Binary[1]	Binomial[1]	Fibonacci[1]	Pairing[2]	Brodal[3][a]	Rank-pairing[5]	Strict Fibonacci[6]
# find-min	    Θ(1)	    Θ(1)	    Θ(1)	        Θ(1)	    Θ(1)	        Θ(1)	        Θ(1)
# delete-min	Θ(log n)	Θ(log n)	O(log n)[b]	    O(log n)	O(log n)	    O(log n)[b]	    O(log n)
# insert	    Θ(log n)	Θ(1)	    Θ(1)	        Θ(1)	    Θ(1)	        Θ(1)	        Θ(1)
# decrease-key	Θ(log n)	Θ(log n)	Θ(1)	        o(log n)	Θ(1)	        Θ(1)[b]	        Θ(1)
# merge	        Θ(n)	    O(log n)	Θ(1)	        Θ(1)	    Θ(1)	        Θ(1)	        Θ(1)
#

from math import log2



class BinomialHeap(object):

    class Node(object):
        def __init__(self, val=None):
            self.value = val
            if val is None:  # Dummy sentinel node at head of list
                self.rank = -1
            else:  # Regular node
                self.rank = 0
                # Rank = Number of children = n. Each child then has rank n - 1
                # as per definition of binomial tree
            self.leftmostchild = None
            self.rightsibling = None
            self.parent = None

        def remove_root(self):
            assert self.next is None
            result = None
            node = self.down
            while node is not None:  # Reverse the order of nodes from descending rank to ascending rank
                next = node.next
                node.next = result
                result = node
                node = next
            return result

    def __init__(self, heaplist_input=None):
        if heaplist_input == None:
            self.heapList = [0]
            self.size = 0
        else:
            self.heapList = [0] + heaplist_input
            self.buildHeap(self.heapList)
            self.size = len(heaplist_input)

    def __swap(self, firstindex, secondindex):
        tmp = self.heapList[secondindex]
        self.heapList[secondindex] = self.heapList[firstindex]
        self.heapList[firstindex] = tmp

    def buildheap(self,array):
        self.ntrees = int(log2(self.size)) + 1
        for i in range(self.ntrees):
            self.treerootpointers[i] = 2**i
        self.minval = float('inf')
        for i in self.treerootpointers:
            if self.heapList[i]<self.minpointer:
                self.minpointer = i
                self.minval = self.heapList[i]

        for i in range(len(self.size)):
            nodeslist = {}
            nodeslist[i] = Node(self.heapList[i])




    def percUp(self, node_index):
        while (node_index - 1) // 2 >= 0:
            if self.heapList[node_index] < self.heapList[(node_index - 1) // 2]:
                self.__swap(node_index, (node_index - 1) // 2)
            node_index = (node_index - 1) // 2

    def insert(self, insertElement):
        self.heapList.append(insertElement)
        self.size = self.size+ 1
        self.percUp(self.size- 1)


# Binomial heap (Python)
#
# Copyright (c) 2014 Project Nayuki
# https://www.nayuki.io/page/binomial-heap
#
# (MIT License)
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
# - The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
# - The Software is provided "as is", without warranty of any kind, express or
#   implied, including but not limited to the warranties of merchantability,
#   fitness for a particular purpose and noninfringement. In no event shall the
#   authors or copyright holders be liable for any claim, damages or other
#   liability, whether in an action of contract, tort or otherwise, arising from,
#   out of or in connection with the Software or the use or other dealings in the
#   Software.
#


class BinomialHeap(object):
    def __init__(self):
        self.head = BinomialHeap.Node()  # Dummy node

    def __len__(self):
        result = 0
        node = self.head.next
        while node is not None:
            result |= 1 << node.rank
            node = node.next
        return result

    def clear(self):
        self.head.next = None

    def enqueue(self, val):
        self._merge(BinomialHeap.Node(val))

    def peek(self):
        if self.head.next is None:
            raise Exception("Empty heap")
        result = None
        node = self.head.next
        while node is not None:
            if result is None or node.value < result:
                result = node.value
            node = node.next
        return result

    def dequeue(self):
        if self.head.next is None:
            raise Exception("Empty heap")
        min = None
        nodebeforemin = None
        prevnode = self.head
        node = self.head.next
        while node is not None:
            if min is None or node.value < min:
                min = node.value
                nodebeforemin = prevnode
            prevnode = node
            node = node.next
        assert min is not None and nodebeforemin is not None

        minnode = nodebeforemin.next
        nodebeforemin.next = minnode.next
        minnode.next = None
        self._merge(minnode.remove_root())
        return min

    # Moves all the values in the given heap into this heap
    def merge(self, other):
        if other is self:
            raise ValueError()
        self._merge(other.head.next)
        other.head.next = None

    # 'other' must be a bare node with no initial dummy node
    def _merge(self, other):
        assert self.head.rank == -1
        this = self.head.next
        self.head.next = None
        prevtail = None
        tail = self.head

        while this is not None or other is not None:
            if other is None or (this is not None and this.rank <= other.rank):
                node = this
                this = this.next
            else:
                node = other
                other = other.next
            node.next = None

            assert tail.next is None
            if tail.rank < node.rank:
                prevtail = tail
                tail.next = node
                tail = node
            elif tail.rank == node.rank + 1:
                assert prevtail is not None
                node.next = tail
                prevtail.next = node
                prevtail = node
            elif tail.rank == node.rank:
                # Merge nodes
                if tail.value <= node.value:
                    node.next = tail.down
                    tail.down = node
                    tail.rank += 1
                else:
                    assert prevtail is not None
                    tail.next = node.down
                    node.down = tail
                    node.rank += 1
                    tail = node
                    prevtail.next = node
            else:
                raise AssertionError()

    # For unit tests
    def check_structure(self):
        head = self.head
        if head.value is not None or head.rank != -1:
            raise AssertionError()
        if head.next is not None:
            if head.next.rank <= head.rank:
                raise AssertionError()
            head.next.check_structure(True)

    class Node(object):
        def __init__(self, val=None):
            self.value = val
            if val is None:  # Dummy sentinel node at head of list
                self.rank = -1
            else:  # Regular node
                self.rank = 0
            self.down = None
            self.next = None

        def remove_root(self):
            assert self.next is None
            result = None
            node = self.down
            while node is not None:  # Reverse the order of nodes from descending rank to ascending rank
                next = node.next
                node.next = result
                result = node
                node = next
            return result

        def check_structure(self, ismain):
            # if self.value is None or self.rank < 0:                raise AssertionError()
            if self.rank >= 1:
                if self.down is None or self.down.rank != self.rank - 1:
                    raise AssertionError()
                self.down.check_structure(False)
                if not ismain:
                    if self.next is None or self.next.rank != self.rank - 1:
                        raise AssertionError()
                    self.next.check_structure(False)
            if ismain and self.next is not None:
                if self.next.rank <= self.rank:
                    raise AssertionError()
                self.next.check_structure(True)


if __name__ == "__main__":
    def test1():
        from PriorityQueue import PriorityQueue
        import random
        print("test1")
        ITERATIONS = 10000
        que = PriorityQueue()
        heap = BinomialHeap()
        length = 0
        for i in range(ITERATIONS):
            if i % 300 == 0:
                print("Progress: {:.0%}".format(float(i) / ITERATIONS))
            op = random.randint(0, 99)

            if op < 1:  # Clear
                heap.check_structure()
                for j in range(length):
                    if heap.dequeue() != que.extractMin():
                        raise AssertionError()
                if not que.empty():
                    raise AssertionError()
                length = 0

            elif op < 2:  # Peek
                heap.check_structure()
                if length > 0:
                    val = que.extractMin()
                    if heap.peek() != val:
                        raise AssertionError()
                    que.insert(val)

            elif op < 60:  # Add
                n = random.randint(1, 100)
                for j in range(n):
                    val = random.randint(0, 9999)
                    que.insert(val)
                    heap.enqueue(val)
                length += n

            elif op < 70:  # Merge
                n = random.randint(1, 100)
                temp = BinomialHeap()
                for j in range(n):
                    val = random.randint(0, 9999)
                    que.insert(val)
                    temp.enqueue(val)
                heap.merge(temp)
                if len(temp) != 0:
                    raise AssertionError()
                length += n

            elif op < 100:  # Remove
                n = min(random.randint(1, 100), length)
                for j in range(n):
                    if heap.dequeue() != que.extractMin():
                        raise AssertionError()
                length -= n

            else:
                raise AssertionError()

            if len(heap) != length:
                raise AssertionError()

        print("Test passed")


    test1()
