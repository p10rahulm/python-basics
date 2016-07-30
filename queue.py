from collections import deque


class Queue(object):
    def __init__(self,queuearray):
        self.queue = deque(queuearray)
        self.empty = self.isempty()

    def isempty(self):
        if len(self.queue) ==0:return True
        else: return False

    def enqueue(self,vertex):
        self.queue.append(vertex)

    def show(self):
        print(self.queue)

    def unqueue(self):
        if len(self.queue) >1:
            return self.queue.popleft()
        elif len(self.queue) == 1:
            self.empty = True
            return self.queue.popleft()
        else:
            print("Cannot Unqueue. Queue is empty")
            return
    def __str__(self):
        return str(self.queue)


'''
Q = Queue(["London","Paris","New York","Delhi"])
Q.show()
Q.enqueue("Madras")
Q.show()
Q.unqueue()
Q.show()
Q.unqueue()
Q.show()
Q.unqueue()
Q.show()
Q.unqueue()
Q.show()
Q.unqueue()
Q.show()
Q.unqueue()
Q.show()
'''