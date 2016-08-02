class Node(object):

    def __init__(self, data, next):
        self.data = data
        self.next = next


class SingleList(object):

    head = None
    tail = None

    def show(self):
        print("Showing list data:")
        current_node = self.head
        while True:
            print("data:",current_node.data, " -> ")
            if current_node.next is not None:
                print("next:",current_node.next.data)
            if current_node == self.tail:
                break

            current_node = current_node.next

    def append(self, data):
        node = Node(data, None)
        if self.head is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
        self.tail = node
        self.tail.next = self.head

    def remove(self, node_value):
        current_node = self.head
        previous_node = None
        nextref = None
        while True:
            if current_node.data == node_value:
                # if this is the first node (head)
                if previous_node is not None:
                    previous_node.next = current_node.next

                else:
                    self.head = current_node.next
                    self.tail.next = current_node.next

            if current_node == self.tail:   break
            # needed for the next iteration
            previous_node = current_node
            current_node = current_node.next


if __name__ == "__main__":

    s = SingleList()
    s.append(31)
    s.append(2)
    s.append(3)
    s.append(4)

    s.show()
    s.remove(31)
    s.remove(3)
    s.remove(2)