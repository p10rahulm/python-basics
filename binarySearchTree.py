import time
starttime = time.time()
class binarySearchTree(object):
    def __init__(self,inputArray = None):
        self.array = inputArray
        if inputArray is None: self.size = 0
        else: self.size = len(inputArray)

    def search


