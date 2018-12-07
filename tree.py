class Tree:
    node_root = None
    
    def __init__(self, nr):
        self.node_root = nr
    def get_root(self):
        return self.node_root
    def set_root(self, node):
        self.node_root = node