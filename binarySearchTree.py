class TreeNode:
    def __init__(self,key,val,left=None,right=None,parent=None,count = 1):
        self.key = key
        self.payload = [val]
        self.leftChild = left
        self.rightChild = right
        self.parent = parent
        self.count = 1
    def hasLeftChild(self):
        return self.leftChild

    def hasRightChild(self):
        return self.rightChild

    def isLeftChild(self):
        return self.parent and self.parent.leftChild == self
    def isRightChild(self):
        return self.parent and self.parent.rightChild == self

    def isRoot(self):
        return not self.parent

    def isLeaf(self):
        return not (self.rightChild or self.leftChild)
    def hasAnyChildren(self):
        return self.rightChild or self.leftChild
    def hasBothChildren(self):
        return self.rightChild and self.leftChild

    def appendValuetoNode(self,value):
        self.count += 1
        self.payload.append(value)
        return 1


    def __iter__(self):
        if self:
            if self.hasLeftChild():
                for elem in self.leftChild:
                    yield elem
            yield self.key
            if self.hasRightChild():
                for elem in self.rightChild:
                    yield elem

    def replaceNodeData(self,key,value,lc,rc):
        self.key = key
        self.count = 1
        self.payload = [value]
        self.leftChild = lc
        self.rightChild = rc
        if self.hasLeftChild():
            self.leftChild.parent = self
        if self.hasRightChild():
            self.rightChild.parent = self

    def findSuccessor(self):
        succ = None
        if self.hasRightChild():
            succ = self.rightChild.findMin()
        else:
            if self.parent:
                   if self.isLeftChild():
                       succ = self.parent
                   else:
                       self.parent.rightChild = None
                       succ = self.parent.findSuccessor()
                       self.parent.rightChild = self
        return succ

    def findMax(self):
        current = self
        while current.hasRightChild():
            current = current.rightChild
        return current

    def findMin(self):
        current = self
        while current.hasLeftChild():
            current = current.leftChild
        return current

    def spliceOut(self):
        if self.isLeaf():
            if self.isLeftChild():
                self.parent.leftChild = None
            else:
                self.parent.rightChild = None
        elif self.hasAnyChildren():
            if self.hasLeftChild():
                if self.isLeftChild():
                    self.parent.leftChild = self.leftChild
                else:
                    self.parent.rightChild = self.leftChild
                self.leftChild.parent = self.parent
            else:
                if self.isLeftChild():
                    self.parent.leftChild = self.rightChild
                else:
                    self.parent.rightChild = self.rightChild
                self.rightChild.parent = self.parent

class BinarySearchTree:

    def __init__(self):
        self.root = None
        self.size = 0

    def length(self):
        return self.size

    def __len__(self):
        return self.size

    def __iter__(self):
        return self.root.__iter__()

    def insert(self,key,val):
        appended =0
        if self.root:
            appended = self._insert(key,val,self.root)
        else:
            self.root = TreeNode(key,val)
        if appended!= 1: self.size = self.size + 1

    def _insert(self,key,val,currentNode):
        if key == currentNode.key:
            appended = currentNode.appendValuetoNode(val)
            return appended
        if key < currentNode.key:
            if currentNode.hasLeftChild():
                self._insert(key,val,currentNode.leftChild)
            else:
                currentNode.leftChild = TreeNode(key,val,parent=currentNode)
        else:
            if currentNode.hasRightChild():
                self._insert(key,val,currentNode.rightChild)
            else:
                currentNode.rightChild = TreeNode(key,val,parent=currentNode)
        return 0

    # __setitem__ overloads the [] operator
    def __setitem__(self,k,v):
        self.insert(k,v)

    def find(self,key):
        if self.root:
            nodefound = self._find(key,self.root)
            if nodefound:
                   return nodefound.payload
            else:
                   return None
        else:
            return None

    def _find(self,key,currentNode):
        if not currentNode:
            return None
        elif currentNode.key == key:
            return currentNode
        elif key < currentNode.key:
            return self._find(key,currentNode.leftChild)
        else:
            return self._find(key,currentNode.rightChild)
    # By implementing the __getitem__ method we can write a Python statement that looks just like we
    # are accessing a dictionary, for example z = myZipTree['Fargo']
    def __getitem__(self,key):
        return self.find(key)
    # __contains__ overloads the in operator
    def __contains__(self,key):
        if self._get(key,self.root):
            return True
        else:
            return False

    def delete(self,key):
        if self.size > 1:
            nodeToRemove = self._find(key,self.root)
            if nodeToRemove:
                self.remove(nodeToRemove)
                self.size = self.size-1
            else:
                raise KeyError('Error, key not in tree')
        elif self.size == 1 and self.root.key == key:
            self.root = None
            self.size = self.size - 1
        else:
            raise KeyError('Error, key not in tree')

    # __delitem__ implements the expression del my_instance[index]
    def __delitem__(self,key):
        self.delete(key)

    def find_successor(self,key):
        current_node = self._find(key,self.root)
        succ = None
        if current_node.hasRightChild():
            succ = current_node.rightChild.findMin()
        else:
            if current_node.parent:
                   if current_node.isLeftChild():
                       succ = current_node.parent
                   else:
                       current_node.parent.rightChild = None
                       succ = current_node.parent.findSuccessor()
                       current_node.parent.rightChild = current_node
        return succ


    def findTreeMin(self):
        current = self.root
        while current.hasLeftChild():
            current = current.leftChild
        return current.payload

    def find_predecessor(self,key):
        current = self._find(key,self.root)
        if current is None: return "Value not found"
        if current.hasLeftChild():
            current = current.leftChild
            while current.hasRightChild():
                current = current.rightChild
            return current.payload
        elif current.parent is not None:
            keystore = current.key
            while current.parent is not None:
                current = current.parent
                if current.key < keystore:
                    return current.payload
            return "Your key is minimum in tree"

        else: return "No predecessor found"



    def findTreeMax(self):
        current = self.root
        while current.hasRightChild():
            current = current.rightChild
        return current.payload

    def remove(self,currentNode):
        if currentNode.isLeaf(): #leaf
            if currentNode == currentNode.parent.leftChild:
                currentNode.parent.leftChild = None
            else:
                currentNode.parent.rightChild = None
        elif currentNode.hasBothChildren(): #interior
            succ = currentNode.findSuccessor()
            succ.spliceOut()
            currentNode.key = succ.key
            currentNode.payload = succ.payload
        else: # this node has one child
            if currentNode.hasLeftChild():
                if currentNode.isLeftChild():
                    currentNode.leftChild.parent = currentNode.parent
                    currentNode.parent.leftChild = currentNode.leftChild
                elif currentNode.isRightChild():
                    currentNode.leftChild.parent = currentNode.parent
                    currentNode.parent.rightChild = currentNode.leftChild
                else:
                    currentNode.replaceNodeData(currentNode.leftChild.key,
                                    currentNode.leftChild.payload,
                                    currentNode.leftChild.leftChild,
                                    currentNode.leftChild.rightChild)
            else:
                if currentNode.isLeftChild():
                    currentNode.rightChild.parent = currentNode.parent
                    currentNode.parent.leftChild = currentNode.rightChild
                elif currentNode.isRightChild():
                    currentNode.rightChild.parent = currentNode.parent
                    currentNode.parent.rightChild = currentNode.rightChild
                else:
                    currentNode.replaceNodeData(currentNode.rightChild.key,
                                    currentNode.rightChild.payload,
                                    currentNode.rightChild.leftChild,
                                    currentNode.rightChild.rightChild)




if __name__ == "__main__":
    import time
    timestart = time.time()
    for i in range(10000):
        mytree = BinarySearchTree()
        mytree[3]="red"
        mytree[4]="blue"
        mytree[6]="yellow"
        mytree[2]="at"
        mytree[2] ="hi"

    print(mytree[6])
    print("2=",mytree[2])
    for i in mytree:
        print(mytree[i])
    print("6.pred = ",mytree.find_predecessor(6))
    print(mytree.findTreeMax())
    print(mytree.findTreeMin())
    print(mytree.root.key)
    mytree.delete(3)
    print()
    for i in mytree:
        print(mytree[i])
    print(mytree.root.key)
    try:
        mytree.delete(5)
    except Exception as error:
        print("not able to delete. error = ",error)
    for i in mytree:
        print(mytree[i])
    print("time taken = ",time.time()-timestart)
