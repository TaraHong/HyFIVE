class Variable():
    def __init__(self,distribution,*args):
        self.dist = distribution
        self.args = args
    def evaluate(self):
        return self.dist(*self.args)
    def __call__(self):
        return self.evaluate()

