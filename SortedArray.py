import time
import quicksort
time = time.time()

class SortedArray(object):
    def __init__(self,inputArray = None):
        if inputArray != None:
            self.array = []
            self.size = 0
        elif type(inputArray) is list:
            self.array = inputArray
            self.sortarray()
            self.size = len(inputArray)
        else: raise TypeError("Unable to initialize, please input list")

    def sortarray(self):
        self.array = quicksort(self.array)

    def show(self):
        print(self.array)

    def inputlist(self,inputArray):
        self.array = inputArray
        self.sortarray()
        self.size = len(inputArray)

    def __str__(self):
        return str(self.array)

    def insertval(self,value):
        rank = self.rank(value)
        newarray = self.array[:rank+1] + [value] + self.array[rank + 1:]
        self.array = newarray
        self.size = self.size +1
        return



    def deleteindex(self,index):
        newarray = self.array[:index] + self.array[index+1:]
        self.array = newarray
        self.size = self.size -1
        return

    def deleteval(self,value):
        index = self.findvalue(value)
        self.deleteindex(index)
        return

    def pop(self,index = None):
        if index > self.size - 1: raise IndexError("choose index lower than size of array")
        if index !=None: self.array.pop(index)
        elif index ==None: self.array.pop()
        self.size -=1
        return

    def push(self,value):
        self.insertval(value)
        return

    def select(self,index):
        return self.array[index]

    def min(self):
        return self.array[0]

    def max(self):
        return self.array[self.size-1]

    def return_predecessor(self,index):
        return self.array[index -1]

    def return_successor(self,index):
        return self.array[index +1]

    def rank(self,value):
        return self.findrank(value,0,self.size - 1)

    def findrank(self,value,minindex,maxindex):
        if minindex == maxindex:
            return minindex
        elif maxindex < minindex:
            return minindex
        for i in range(minindex,maxindex+1):
            if value == self.array[maxindex+1//2]:
                return (maxindex+1)//2
            elif value > self.array[(maxindex+1)//2]:
                return self.findvalue(value,(maxindex+1)//2 +1,maxindex)
            else:
                return self.findvalue(value,minindex,(maxindex+1)//2)

    def find(self,value):
        return self.findvalue(value,0,self.size-1)

    def findvalue(self,value,minindex,maxindex):
        if minindex == maxindex:
            if value == self.array[minindex] :
                return minindex
            else:
                return "value not found"
        elif maxindex < minindex :
            return "value not found"
        for i in range(minindex,maxindex+1):
            if value == self.array[maxindex+1//2]:
                return (maxindex+1)//2
            elif value > self.array[(maxindex+1)//2]:
                return self.findvalue(value,(maxindex+1)//2 +1,maxindex)
            else:
                return self.findvalue(value,minindex,(maxindex+1)//2)

if __name__ == "__main__":
    a = SortedArray()
