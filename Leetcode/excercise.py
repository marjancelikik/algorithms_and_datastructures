
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


def delete_node(head: ListNode, val: int):
    if head is None:
        return None
    
    if head.val == val:
        return head.next

    n = head

    while n.next is not None:
        if n.next.val == val:
            n.next = n.next.next
            return head
        
        n = n.next
    
    return head

# head = ListNode(1)
# head.next = ListNode(2)
# head.next.next = ListNode(3)

# head = delete_node(head, 1)

# print(head.val)


# 1->2->3, val = 1

# 1->2->3, val = 2

# head = 1
# head.next = 2
# head.next <- 3
# head <- 3



# 1->2, val = 2

# head = 1
# head.next <- 2
# head.next = None

# head <- None


# Generate some test cases for the function delete_node above
def test_delete_node():
    head = ListNode(1)
    head.next = ListNode(2)
    head.next.next = ListNode(3)

    head = delete_node(head, 1)

    assert head.val == 2
    assert head.next.val == 3

    head = ListNode(1)
    head.next = ListNode(2)
    head.next.next = ListNode(3)

    head = delete_node(head, 2)

    assert head.val == 1
    assert head.next.val == 3

    head = ListNode(1)
    head.next = ListNode(2)

    head = delete_node(head, 2)

    assert head.val == 1
    assert head.next == None

    head = ListNode(1)
    head.next = ListNode(2)

    head = delete_node(head, 1)

    assert head.val == 2
    assert head.next == None

    head = ListNode(1)

    head = delete_node(head, 1)

    assert head == None

    print("All test cases pass")

def stack_excerise():

    stack = [1, 2, 3]

    stack.append(4)

    print(stack)
    print(stack.pop())

def queue_excerise():

    from collections import deque

    deque = deque([1, 2, 3])

    print(deque)
    deque.append(4)
    print(deque)
    deque.popleft()
    print(deque)
    deque.prepend(0)

class TreeNode:
    def __init__(self, val: int):
        self.val = val
        self.left = None
        self.right = None

def _find(node: TreeNode, val):

    if node is None:
        return None
    
    ancestor = None
    n = node
    while n is not None:
        ancestor = n
        if n.val == val:
            return n
        elif val < n.val:
            n = n.left
        else:
            n = n.right
    
    return ancestor

def find(node: TreeNode, val):

    if node is None:
        return None

    n = _find(node, val)
    if n is not None and n.val == val:
        return n
    
def insert(node: TreeNode, val) -> tuple[TreeNode, bool]:

    if node is None:
        return None, False

    n = _find(node, val)

    if n is None:
        return None, False

    if n is not None and n.val == val:
        return None, False
    
    n_new = TreeNode(val)
    if val < n.val:
        n.left = n_new
    else:
        n.right = n_new
    
    return n_new, True
  
def print_tree(node: TreeNode, traversed_prefix="") -> str:
    if node is None:
        return traversed_prefix
    
    traversed_prefix = print_tree(node.left, traversed_prefix)
    traversed_prefix += str(node.val) + ", "
    traversed_prefix = print_tree(node.right, traversed_prefix)

    return traversed_prefix

def get_depth_of_tree(node: TreeNode):

    if node is None:
        return 0

    depth = 1 + max(get_depth_of_tree(node.left), get_depth_of_tree(node.right))

    return depth

def is_balanced_tree(node: TreeNode) -> bool:

    if node is None:
        return True
    
    depth_left = get_depth_of_tree(node.left)
    depth_right = get_depth_of_tree(node.right)

    return is_balanced_tree(node.left) and is_balanced_tree(node.right) and abs(depth_left - depth_right) <= 1

def create_bst(sorted_list: list, left: int, right: int) -> TreeNode:

    if left > right:
        return None
    
    median = (left + right) // 2
    root = TreeNode(sorted_list[median])
    root.left = create_bst(sorted_list, left, median - 1)
    root.right = create_bst(sorted_list, median + 1, right)

    return root

def sum_nodes_tree(root: TreeNode) -> int:

    if root is None:
        return 0
    
    return root.val + sum_nodes_tree(root.left) + sum_nodes_tree(root.right)

def practice_tree():
    n = TreeNode(10)
    insert(n, 5)
    insert(n, 20)
    insert(n, 1)
    insert(n, 7)
    insert(n, 15)
    insert(n, 30)
    insert(n, 11)

    print(print_tree(n))
    print(get_depth_of_tree(n))
    print(is_balanced_tree(n))

    insert(n, 40)
    insert(n, 50)
    insert(n, 60)
    insert(n, 70)
    print(is_balanced_tree(n))

    a = [1, 5, 10, 20, 30, 40]
    n1 = create_bst(a, 0, len(a) - 1)
    print(print_tree(n1))
    print(get_depth_of_tree(n1))
    print(is_balanced_tree(n1))
    print(f"{sum_nodes_tree(n1)}, {sum(a)}")


def practice_heap():
    
    import heapq

    heap = []

    heapq.heappush(heap, 10)
    heapq.heappush(heap, 5)
    heapq.heappush(heap, 20)
    heapq.heappush(heap, 4)
    heapq.heappush(heap, 6)
    heapq.heappush(heap, 17)

    print(heap)

    x = heapq.heappop(heap)

    print(x)
    print(heap)


def find_k_most_frequent(l: list, topk: int):

    class Pair:
        def __init__(self, frequency: int, val: int):
            self.frequency = frequency
            self.val = val

        def __lt__(self, other):
            return self.frequency > other.frequency

    from collections import Counter

    frequency_list = []
    counter = Counter(l)
    for k, v in counter.items():
        print((v, k))
        frequency_list.append(Pair(v, k))
    
    import heapq

    heap = []

    for pair in frequency_list:

        if len(heap) < topk:
            heapq.heappush(heap, pair)
        else:
            if heap[0].frequency < pair.frequency:
                heapq.heappop(heap)
                heapq.heappush(heap, pair)
        
    return [(x.val, x.frequency) for x in heap]

# print(find_k_most_frequent([1, 2, 1, 1, 2, 1, 1, 2, 2, 2, 3, 4, 4, 7, 6, 3], topk=3))

def dfs(graph: dict, root: int):

    def visit(node):
        print(node)

    visited = set()

    def _dfs(graph: dict, root: int):
    
        visit(root)
        visited.add(root)

        for adj_node in graph.get(root, []):
            if adj_node not in visited:
                _dfs(graph, adj_node)

    _dfs(graph, root)


def bfs(graph: dict, root: int):

    def visit(node):
        print(node)

    from collections import deque
    queue = deque()
    visited = set()
    
    visit(root)
    queue.append(root)

    while len(queue) > 0:
        
        node = queue.popleft()

        for adj_node in graph.get(node, []):
            if adj_node not in visited:
                visit(adj_node)
                visited.add(adj_node)
                queue.append(adj_node)


def topological_sort_dfs(graph):
    visited = set()
    stack = []

    def dfs(node):
        if node in visited:
            return
        visited.add(node)
        for neighbor in graph.get(node, []):
            dfs(neighbor)
        stack.append(node)

    for node in graph:
        if node not in visited:
            dfs(node)

    return stack[::-1]  # Reverse the stack for topological order


def practice_graph():

    graph = {
        0: [1, 4, 5],
        5: [],
        1: [3, 4],
        2: [1],
        3: [2, 4],
        4: []
    }

    dfs(graph=graph, root=0)
    print("------------")
    bfs(graph=graph, root=0)


# practice_graph()
practice_tree()
