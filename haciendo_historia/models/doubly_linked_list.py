from models.node import Node


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def append(self, value):
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.length += 1

    def prepend(self, value):
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self.length += 1

    def traverse_to_index(self, index):
        current_node = self.head
        i = 0
        while i != index:
            current_node = current_node.next
            i += 1
        return current_node

    def insert(self, index, value):
        if index == 0:
            self.prepend(value)
        elif index >= self.length:
            self.append(value)
        else:
            new_node = Node(value)
            leader = self.traverse_to_index(index - 1)
            follower = leader.next
            leader.next = new_node
            new_node.prev = leader
            new_node.next = follower
            follower.prev = new_node
            self.length += 1

    def remove(self, index):
        if self.length == 0:
            return None
        if index == 0:
            removed = self.head
            self.head = self.head.next
            if self.head:
                self.head.prev = None
            else:
                self.tail = None
            self.length -= 1
            return removed.value
        elif index >= self.length - 1:
            removed = self.tail
            self.tail = self.tail.prev
            if self.tail:
                self.tail.next = None
            else:
                self.head = None
            self.length -= 1
            return removed.value
        else:
            leader = self.traverse_to_index(index - 1)
            node_to_remove = leader.next
            follower = node_to_remove.next
            leader.next = follower
            follower.prev = leader
            self.length -= 1
            return node_to_remove.value

    def to_list(self):
        result = []
        current_node = self.head
        while current_node is not None:
            result.append(current_node.value)
            current_node = current_node.next
        return result

    def to_list_reversed(self):
        result = []
        current_node = self.tail
        while current_node is not None:
            result.append(current_node.value)
            current_node = current_node.prev
        return result

    def search(self, value):
        current_node = self.head
        index = 0
        while current_node is not None:
            if current_node.value == value:
                return index
            current_node = current_node.next
            index += 1
        return -1
