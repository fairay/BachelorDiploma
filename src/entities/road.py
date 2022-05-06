class Road(object):
    def __init__(self, dist=1.0, time=1.0):
        self.dist: float = dist
        self.time: float = time

    def __repr__(self):
        return f'↔{self.dist} ⌛{self.time}'
