class Node:
    def __init__(self, question=None, answer=None):
        self.question = question
        self.answer = answer
        self.yes = None
        self.no = None

    def is_leaf(self):
        return self.answer is not None