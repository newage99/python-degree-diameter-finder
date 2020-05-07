class IdTree:

    def __init__(self, id):
        self.id = id
        self.children = []

    def add_child(self, child_id_tree):
        self.children.append(child_id_tree)

    def load(self, json):
        pass

    def dump(self):
        pass
