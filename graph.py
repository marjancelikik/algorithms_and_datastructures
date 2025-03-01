
def dfs(graph: dict, root):
    from collections import deque
    pred = {}
    color = dict()
    top_order = deque()
    for node in graph.keys():
        color[node] = 0

    def visit(node):
        print("visiting {}".format(node))
        color[node] = 1

    def _dfs(node) -> bool:
        if color[node] == 1:
            return False

        if color[node] == 0:
            visit(node)
            for child in graph.get(node, []):
                pred[child] = node
                if not _dfs(child):
                    return False

            color[node] = 2
            top_order.appendleft(node)
        return True

    for node in graph.keys():
        if color[node] == 0:
            if not _dfs(node):
                return None

    return pred, color, top_order


def print_pred(pred: dict, node):
    print(node)
    p_node = pred.get(node)
    if p_node is not None:
        print_pred(pred, p_node)


graph = {
    0: [1],
    1: [3],
    2: [0],
    3: [4],
    4: []
}

result = dfs(graph, root=0)

if not result:
    print("Graph has a cycle!")
else:
    pred, color, top_order = result
    print(color)
    print(top_order)


def bfs(graph: dict, root):
    def visit(node):
        print(node)

    from collections import deque
    queue = deque()
    visited = set()

    queue.append(root)

    while len(queue) > 0:
        node = queue.popleft()
        visit(node)
        visited.add(node)
        for child in graph.get(node, []):
            if child not in visited:
                queue.append(child)


graph_1 = {
    0: [1, 2, 3, 4],
    1: [6],
    2: [5],
    3: [8],
    4: [7],
    7: [9]
}

# bfs(graph_1, 0)
