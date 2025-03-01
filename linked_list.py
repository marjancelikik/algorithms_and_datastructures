class LinkedList:

    class Node:
        def __init__(self, data=None, next=None):
            self.data = data
            self.next = next

    def __init__(self):
        self.head = LinkedList.Node()

    def append(self, data):
        head = self.head

        while head.next is not None:
            head = head.next

        head.next = LinkedList.Node(data=data)

    def delete_node(self, data):

        node = self.head
        while node.next is not None:
            if node.next.data == data:
                node.next = node.next.next
                return node
            node = node.next

        return None

    def reverse(self):

        new_ll = LinkedList()
        node = self.head.next
        head = None
        last_node = None
        while node is not None:
            n = LinkedList.Node(node.data)
            print(node.data)
            if head is not None:
                print("-> {}".format(head.data))
            last_node = n
            n.next = head
            head = node
            node = node.next

        new_ll.head.next = last_node
        return new_ll

    def print(self):

        node = self.head.next
        while node is not None:
            print(node.data)
            node = node.next

        print("---")


# ll = LinkedList()
# ll.append(1)
# ll.append(2)
# ll.append(3)
# ll.append(4)
# ll_r = ll.reverse()
# ll_r.print()
#
# n1 = LinkedList.Node(10)
# n2 = LinkedList.Node(12)
# hash_node = {
#     n1: 10,
#     n2: 12
# }
# print(hash_node[n1])
# print(hash_node[n2])


class Node:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next


def reverse_list(head: Node):

    if head is None:
        return None

    prev = None
    node = head

    while node is not None:

        next_node = node.next
        node.next = prev

        prev = node
        node = next_node

    return prev


def print_list(head: Node):
    while head is not None:
        print(f"{head.val}->")
        head = head.next


head = Node(1, next=Node(2, next=Node(3, next=Node(4))))

print_list(reverse_list(head))
