class Goal:
    def __init__(self, name, value, max_value=9999999999):
        self.name = name
        self.value = value
        self.rate = 1
        self.max_value = max_value

    def clone(self):
        g = Goal(self.name[:], self.value)
        g.rate = self.rate
        return g

    def modify_value(self, mod):
        self.value = min(max(self.value + mod, 0), self.max_value)

    def set_value(self, v):
        self.value = min(max(v, 0), self.max_value)