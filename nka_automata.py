class NKAutomata:
    def __init__(self, states, symbols):
        self.states = states
        self.symbols = symbols

    def __repr__(self):
        s = 'NKA: \n'
        for i, item in self.states.items():
            s += item.__repr__() + '\n'
        return s