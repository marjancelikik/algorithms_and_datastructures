class TreeNode:
    def __init__(self, value=None, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def print_in_order(root: TreeNode):
    if root is not None:
        print_in_order(root.left)
        print(root.value)
        print_in_order(root.right)


def print_pre_order(root: TreeNode):
    if root is not None:
        print(root.value)
        print_in_order(root.left)
        print_in_order(root.right)


def print_post_order(root: TreeNode):
    if root is not None:
        print_in_order(root.left)
        print_in_order(root.right)
        print(root.value)


def _find(root: TreeNode, val):
    if root is None:
        return None
    node = root
    ancestor = None
    while node is not None and node.value != val:
        ancestor = node
        if val > node.value:
            node = node.right
        else:
            node = node.left

    if node is not None:
        return node
    else:
        return ancestor


def insert(root: TreeNode, val) -> (TreeNode, bool):
    node = _find(root, val)
    if node is None:
        return None, False
    if node.value == val:
        return node, False
    else:
        new_node = TreeNode(val)
        if val > node.value:
            node.right = new_node
        else:
            node.left = new_node
        return new_node, True


def find(root: TreeNode, val) -> TreeNode:
    node = _find(root, val)
    if node is not None and node.value == val:
        return node
    else:
        return None


def create_bst(array: list, left: int, right: int):
    if left > right:
        return None
    median = (left + right) // 2
    root = TreeNode(array[median],
                    left=create_bst(array, left, median - 1),
                    right=create_bst(array, median + 1, right))
    return root


def traverse_in_order_iterative(root: TreeNode):

    stack = []
    node = root

    while len(stack) > 0 or node is not None:

        if node is not None:
            stack.append(node)
            node = node.left
        else:
            node = stack.pop()
            print(node.value)  # visit
            node = node.right


root = TreeNode(value=100)
insert(root, 50)
insert(root, 200)
insert(root, 40)
insert(root, 90)
insert(root, 200)
insert(root, 101)

# print_pre_order(root)

root1 = create_bst([1, 5, 10, 15, 20, 25, 30], 0, 6)
# print_in_order(root1)

traverse_in_order_iterative(root1)


def get_tree_height(root: TreeNode) -> int:
    if root is None:
        return 0
    return 1 + max(get_tree_height(root=root.left), get_tree_height(root=root.right))


def is_balanced(root: TreeNode) -> bool:
    if root is None:
        return True

    height_left = get_tree_height(root.left)
    height_right = get_tree_height(root.right)
    return abs(height_left - height_right) <= 1 and is_balanced(root.left) and is_balanced(root.right)


root2 = TreeNode(value=0)
insert(root2, 1)
insert(root2, 2)
insert(root2, 3)
insert(root2, 4)
insert(root2, 5)
insert(root2, 6)


# print(get_tree_height(root2))
# print(is_balanced(root2))
