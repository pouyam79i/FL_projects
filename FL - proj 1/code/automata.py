# Coded by Pouya Mohammadi
# here we have a base for our machines

class Automata:
    
    def __init__(self) -> None:
        super().__init__()
        self.ready = False
        self.configFile = None
        self.alphabet = []
        self.states = []
        self.startStates = []
        self.terminateStates = []
        self.rules = {}
    
    # read config file for our machine
    def buildMachine(self, configAddr: str) -> None:
        # read filles
        try:
            with open(configAddr, encoding='UTF-8') as file:
                lines = [line.rstrip() for line in file]
                self.configFile = configAddr
                self.alphabet = lines[0].split(' ')
                self.states = lines[1].split(' ')
                self.startStates = lines[2].split(' ')
                self.terminateStates = lines[3].split(' ')
                for rule in lines[4:]:
                    startState, passingStr, nextState = rule.split(' ')
                    if startState not in self.rules.keys():
                        self.rules[startState] = {}
                    if passingStr not in self.rules[startState].keys():
                        self.rules[startState][passingStr] = []
                    self.rules[startState][passingStr].append(nextState)
                self.ready = True
                print('your machine is ready!')
                print('Alphabet:')
                print(self.alphabet)
                print('States:')
                print(self.states)
                print('Start States:')
                print(self.startStates)
                print('Terminate States:')
                print(self.terminateStates)
                print('Rules:')
                print(self.rules)      
        except:
            self.ready = False
            self.configFile = None
            self.alphabet = []
            self.states = []
            self.startStates = []
            self.terminateStates = []
            self.rules = {}
            print('failed to read machine config file!')
        
    # read string and check if machine accepts the lang. 
    def readString(self, startState: str, data: str) -> bool:
        print("Automata.readString() is not implemented!")
