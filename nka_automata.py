class NKAutomata:
    def __init__(self, states, symbols):
        self.states = states
        self.symbols = symbols

    def to_dka(self):
        return 'konverzia'

    def __repr__(self):
        s = 'NKA: \n'
        for i in self.states:
            s += i.__repr__() + '\n'
        return s
