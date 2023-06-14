# Coded by Pouya Mohammadi
# Here we have a simple DFA builder
# 1- It Reads NFA config
# 2- builds NFA according to that config
# 3- now we can use this NFA!

from automata import Automata
from dfa import DFA

# this is an NFA machine
class NFA(Automata):
    
    def __init__(self) -> None:
        super().__init__()
        self.DFA = DFA()
    
    # builds a NFA machine according to config file data
    def buildMachine(self, configAddr: str) -> None:
        res = super().buildMachine(configAddr)
        if not res:
            self.DFA = DFA()
        return res
    
    # TODO: transform a given NFA to DFA machine
    # TODO: when dfa is built set dfa.ready = true
    def transformToDFA(self) -> DFA:
        if not self.ready:
            print('not a given machine')
            self.DFA = DFA()
            return False
        
        
# Run app main
if __name__ == "__main__":
    machine = NFA()
    machine.buildMachine('../NFA_Input_2.txt')
    dfa_eq = machine.transformToDFA()
    if not dfa_eq.ready:
        print('No DFA equivalent is given!')
        exit()
    print('now lets try an input using equivalent DFA machine!')
    print('This app is case sensitive!')
    startState = input('plz input a start state:').strip()
    data = input('plz input data:').strip()
    dfa_eq.readString(startState, data)
    