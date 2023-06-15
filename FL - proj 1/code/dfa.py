from automata import Automata

# this is a simple DFA machine
class DFA(Automata):
    
    def __init__(self) -> None:
        super().__init__()

    # checks if this DFA machine accepts given start state and string data
    def readString(self, startState: str, data: str) -> bool:
        if not self.ready:
            print('machine is not ready')
            return False
        tracker = []
        if startState not in self.startStates:
            print('{} is not a start state in this machine!'.format(startState))
            return False
        tracker.append('-> ' + startState)
        prevState = startState
        for c in data:
            if c not in self.alphabet:
                print('This machine does not accept this string data!')
                print('reason:')
                print('{} is not in allowed alphabet')
                return False
            if c in self.rules[prevState].keys():
                nextState = self.rules[prevState][c][0]
                tracker.append(prevState + ' - {} -> '.format(c) + nextState)
                prevState = nextState
            else:
                print('This machine does not accept this string data!')
                print('reason:')
                print('from state {} we can\'t go to any other state using character {}.'.format(prevState, c))
                return False
        if prevState not in self.terminateStates:
            print('This machine does not accept this string data!')
            print('reason:')
            print('{} is not a terminate state'.format(prevState))
            return False
        print('This machine accepts this string data')
        print('Check tracker:')
        for track in tracker:
            print(track)
        return True
    
# Run app main
if __name__ == "__main__":
    machine = DFA()
    machine.buildMachine('../DFA_Input_1.txt')
    print('This app is case sensitive!')
    startState = input('plz input a start state:').strip()
    data = input('plz input data:').strip()
    machine.readString(startState, data)
    