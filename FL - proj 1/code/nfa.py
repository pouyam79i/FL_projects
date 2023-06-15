import itertools
import json
from automata import Automata
from dfa import DFA

# this class transforms given NFA to DFA
class NFAtoDFA:
    
    def __init__(self) -> None:
        self.unitStateEpsilonClosure = {}
        self.visited = {}
        self.nfaEpsilonClosureDict = {}
    
    def objectFA(self, s,a,tm,ss,fs):
        return {
            'states': s,
            'alphabet': a,
            'transition_matrix': tm,
            'start_states': ss,
            'terminate_states':fs
        }

    def computeNfaEpsilonClosureDict(self, nfaState, nfaTransitionMatrix):
        if self.visited[nfaState]:
            return self.nfaEpsilonClosureDict[nfaState]
        self.visited[nfaState]=True
        self.nfaEpsilonClosureDict[nfaState] = [nfaState]
        for arc in nfaTransitionMatrix:
            [ss, a, fs] = arc
            if (a != 'λ') or (ss != nfaState):
                continue
            children = self.computeNfaEpsilonClosureDict(fs,nfaTransitionMatrix)
            for child in children:
                if child not in self.nfaEpsilonClosureDict[nfaState]:
                    self.nfaEpsilonClosureDict[nfaState].append(child)
        return self.nfaEpsilonClosureDict[nfaState]

    def epsilonClosure(self, stateList):
        returnState = []
        for st in stateList:
            currentEpsilon = self.unitStateEpsilonClosure[st]
            for cst in currentEpsilon:
                if cst not in returnState:
                    returnState.append(cst)
        return returnState

    def allStatesCombination(self, nfaSTATES):
        return_state = []
        for i in range(len(nfaSTATES)+1):
            combination = [ list(tup) for tup in list(itertools.combinations(nfaSTATES,i))]
            return_state += combination
        return return_state

    def getFinalState(self, nfaFinalStates,dfaStates):
        returnState = []
        for st in dfaStates:
            for fst in nfaFinalStates:
                if (st not in returnState)and(fst in st):
                    returnState.append(st)
                    break
        return returnState

    def getTransitionedState(self, nfaTransitionMatrix, state, letter):
        ts = []
        for st in state:
            for arc in nfaTransitionMatrix:
                [ss, a, fs] = arc
                if (a != letter) or (ss != st):
                    continue
                if fs not in ts:
                    ts.append(fs)
        return ts

    def formTransitionMatrix(self, nfaTransitionMatrix, dfaStates, dfaLetters):
        tm = []
        for st in dfaStates:
            for a in dfaLetters:
                transitionedState = self.getTransitionedState(nfaTransitionMatrix, st, a)
                tm.append([st,a,self.epsilonClosure(transitionedState)])
        return tm

    def convertNFAToDFA(self, NFA):
        DFA_L = NFA['alphabet'][:]
        DFA_S = self.allStatesCombination(NFA['states'])
        DFA_FS = self.getFinalState(NFA['terminate_states'],DFA_S)
        
        for st in NFA['states']:
            for st1 in NFA['states']:
                self.visited[st1] = False
                self.nfaEpsilonClosureDict[st1]=[]
            self.unitStateEpsilonClosure[st] = self.computeNfaEpsilonClosureDict(st,NFA['transition_matrix'])

        DFA_SS = [ self.epsilonClosure([sst]) for sst in NFA['start_states'] ]
        DFA_TM = self.formTransitionMatrix(NFA['transition_matrix'], DFA_S, DFA_L)

        return self.objectFA(DFA_S,DFA_L,DFA_TM,DFA_SS,DFA_FS)

    # Use this method to transform NFA to DFA
    def TransformNFAtoDFA(self, nfa):
        print("Transforming NFA to DFA")        
        if not nfa.ready:
            return None 

        s = nfa.states
        a = nfa.alphabet
        # TODO: convert logic
        tm = []
        for state in nfa.rules:
            for movement in nfa.rules[state]:
                for next_state in nfa.rules[state][movement]:
                    tm.append([state, movement, next_state])
        ss = nfa.startStates
        fs = nfa.terminateStates
        given_nfa = self.objectFA(s, a, tm, ss, fs)
        finalDFA = self.convertNFAToDFA(given_nfa)
        print("DFA result - not simplified:")        
        print(finalDFA)
        # see results in json file
        with open('out/dfa_res.json', "w+") as outfile: 
            json.dump(finalDFA, outfile, indent=2)
        return finalDFA

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
    
    def transformToDFA(self) -> DFA:
        if not self.ready:
            print('not a given machine')
            self.DFA = DFA()
            return self.DFA
        transformer = NFAtoDFA()
        dfa_trans_res = transformer.TransformNFAtoDFA(self)
        # TODO: update DFA obj with given result and return it
        return self.DFA       
              
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
      