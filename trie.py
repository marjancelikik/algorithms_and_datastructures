class TrieNode:
    def __init__(self, terminal=False):
        self.children = dict()
        self.terminal = terminal
        for c in range(ord('a'), ord('z')):
            self.children[chr(c)] = None


def insert_word(root: TrieNode, word: str):
    node = root
    for i, c in enumerate(word):
        if node.children[c] is None:
            node.children[c] = TrieNode(terminal=i == len(word) - 1)
        node = node.children[c]


def lookup_word(root: TrieNode, word: str) -> bool:
    if root is None:
        return False
    node = root
    for c in word:
        node = node.get(c)
        if node is None:
            return False

    return True


def print_trie(root: TrieNode, prefix: str):
    node = root
    if node is None:
        return

    for chr, child in node.children.items():
        if child is not None:
            if child.terminal:
                print(prefix + chr)
            else:
                print_trie(child, prefix + chr)


root = TrieNode()
insert_word(root, "marjan")
insert_word(root, "marketing")
insert_word(root, "marc")
insert_word(root, "kristin")
print_trie(root, "")
