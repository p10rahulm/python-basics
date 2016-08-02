class Node(object):

    def __init__(self, data, prev, next):
        self.data = data
        self.prev = prev
        self.next = next

    # __str__ returns string equivalent of Object
    def __str__(self):
        return "Node[Data = %s]" % (self.data,)

class DoubleList(object):
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, data):
        new_node = Node(data, None, None)
        if self.head is None:
            self.head = self.tail = new_node
            new_node.next = new_node
            new_node.prev = new_node
        else:
            new_node.prev = self.tail
            new_node.next = self.head
            self.tail.next = new_node
            self.head.prev = new_node
            self.tail = new_node

    def remove(self, node_value):
        current_node = self.head
        while True: #current_node is not None:
            if current_node.data == node_value:
                # if it's not the first element
                if current_node is self.head:
                    self.head = current_node.next
                current_node.prev.next = current_node.next
                current_node.next.prev = current_node.prev
                #else:
                    # otherwise we have no prev (it's None), head is the next one, and prev becomes None
                #    self.head = current_node.next
                #    current_node.next.prev = None
            if current_node == self.tail: break

            current_node = current_node.next

    def show(self):
        print("Show list data:")
        current_node = self.head
        while True:
            print("prev:",current_node.prev.data if hasattr(current_node.prev, "data") else None,)
            print("data:",current_node.data,)
            print("next:",current_node.next.data if hasattr(current_node.next, "data") else None)
            if current_node == self.tail: break
            current_node = current_node.next
        #print("*"*50)

if __name__ == "__main__":
    d = DoubleList()

    d.append(5)
    d.append(6)
    d.append(50)
    d.append(30)

    d.show()

    d.remove(50)
    d.remove(5)

    #d.show()
