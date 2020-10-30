class FilterStage:
    def __init__(self, p1 = '-', p2 = '-'):
        self.pole1 = p1
        self.pole2 = p2

    def setPoles(self, p1, p2):
        self.pole1 = p1
        self.pole2 = p2

    def getPoles(self):
        return self.pole1, self.pole2