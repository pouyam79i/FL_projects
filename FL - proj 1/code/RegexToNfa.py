import sys
import json
from nfa import NFA

class REtoNFA:
    
    def __init__(self) -> None:
        pass

    def objectNFA(self, s,a,tm,ss,fs):
        return {
            'states': s,
            'alphabet': a,
            'transition_matrix': tm,
            'start_states': ss,
            'terminate_state':fs
        }

    def unitLenRegexToNFA(self, alphabet):
        s = ["Q0","Q1"]
        a = [alphabet]
        tm = [
            ["Q0",alphabet,"Q1"],
        ]
        ss = ["Q0"]
        fs = ["Q1"]
        return self.objectNFA(s, a, tm, ss, fs)

    def concatenationNFA(self, NFA1, NFA2):
        # Making `a` array
        a = [ alphabet for alphabet in NFA1['alphabet']]
        for a in NFA2['alphabet']:
            if a not in a:
                a.append(a)

        # Making `s, ss and fs` array
        s = []
        ss = []
        fs = []
        tm = []
        for i in range(len(NFA1['states'])):
            current_state = NFA1['states'][i]
            s.append(current_state)
            if current_state in NFA1['start_states']:
                ss.append(current_state)

        for i in range(len(NFA2['states'])):
            current_state = NFA2['states'][i]
            effective_state = "Q"+str(i+len(NFA1['states']))
            s.append(effective_state)
            if current_state in NFA2['terminate_state']:
                fs.append(effective_state)
            
            if current_state in NFA2['start_states']:
                for nfa1_final_state in NFA1['terminate_state']:
                    tm.append([nfa1_final_state,'λ',effective_state])

        # Making `tm` array
        for arc in NFA1['transition_matrix']:
            tm.append(arc)
        
        for arc in NFA2['transition_matrix']:
            [os, il, ns] = arc
            n_os = 'Q'+ str(int(os[1:])+len(NFA1['states']))
            n_ns = 'Q'+ str(int(ns[1:])+len(NFA1['states']))
            tm.append([n_os, il, n_ns ])
        
        return self.objectNFA(s, a,tm, ss, fs)

    def unionNFA(self, NFA1, NFA2):
        # Making `a` array
        a = [ alphabet for alphabet in NFA1['alphabet']]
        for a in NFA2['alphabet']:
            if a not in a:
                a.append(a)

        # Making `s, ss and fs` array
        s = ["Q0"]
        ss = ["Q0"]
        fs = []
        tm = []

        for i in range(len(NFA1['states'])):

            current_state = NFA1['states'][i]
            effective_state = 'Q'+str(i+1)
            s.append(effective_state)

            if current_state in NFA1['terminate_state']:
                fs.append(effective_state)
            if current_state in NFA1['start_states']:
                tm.append(['Q0','λ',effective_state])


        for i in range(len(NFA2['states'])):

            current_state = NFA2['states'][i]
            effective_state = "Q"+str(i+1+len(NFA1['states']))
            s.append(effective_state)

            if current_state in NFA2['terminate_state']:
                fs.append(effective_state)
            if current_state in NFA2['start_states']:
                tm.append(['Q0','λ',effective_state])
        
        # Making `tm` array
        for arc in NFA1['transition_matrix']:
            [os, il, ns] = arc
            n_os = 'Q'+ str(1+int(os[1:]))
            n_ns = 'Q'+ str(1+int(ns[1:]))
            tm.append([n_os, il, n_ns ])
        
        for arc in NFA2['transition_matrix']:
            [os, il, ns] = arc
            n_os = 'Q'+ str(1+int(os[1:])+len(NFA1['states']))
            n_ns = 'Q'+ str(1+int(ns[1:])+len(NFA1['states']))
            tm.append([n_os, il, n_ns ])
        
        return self.objectNFA(s, a, tm, ss, fs)

    def starNFA(self, NFA):
        s = ['Q0']
        for i in range(len(NFA['states'])):
            effective_state = 'Q'+str(i+1)
            s.append(effective_state)
        
        index = 1+len(NFA['states'])
        only_final_state = 'Q'+str(index)
        s.append(only_final_state)

        a = [ letter for letter in NFA['alphabet'] ]
        ss = ['Q0']
        fs = [only_final_state]

        tm = []
        for arc in NFA['transition_matrix']:
            [os, il, ns] = arc
            n_os = 'Q'+ str(1+int(os[1:]))
            n_ns = 'Q'+ str(1+int(ns[1:]))
            tm.append([n_os, il, n_ns ])
        
        for st_state in NFA['start_states']:
            tm.append(['Q0','λ','Q'+ str(1+int(st_state[1:]))])
        tm.append(['Q0','λ',only_final_state])

        for fn_state in NFA['terminate_state']:
            tm.append(['Q'+ str(1+int(fn_state[1:])),'λ',only_final_state])
            for st_state in NFA['start_states']:
                tm.append(['Q'+ str(1+int(fn_state[1:])),'λ','Q'+ str(1+int(st_state[1:]))])
        
        return self.objectNFA(s, a, tm, ss, fs)

    def isAlphabet(self, character):
        flag = False
        if (character>='a')and(character<='z'):
            flag = True
        elif (character>='0')and(character<='9'):
            flag = True
        return flag

    def add_dot(self, regex):
        indices = []
        new_regex = regex[:]
        for i in range(len(regex)-1):
            cc = regex[i]
            cn = regex[i+1]
            if self.isAlphabet(cc) or (cc==')') or (cc=='*'):
                if self.isAlphabet(cn) or cn=='(':
                    indices.append(i)
        
        for i in range(len(indices)):
            index = indices[i]
            new_regex = new_regex[:index+i+1]+"."+new_regex[index+i+1:]
        return new_regex

    def infixToPostfix(self, regex):
        precedence ={
            '*':3,
            '.':2,
            '+':1
        }
        stack = []
        postfixRegex = ""
        for char in regex:
            if self.isAlphabet(char) or (char=='*'):
                postfixRegex += char
            elif char=='(':
                stack.append(char)
            elif char==')':
                while( (len(stack)!=0) and (stack[-1]!='(') ):
                    postfixRegex += stack.pop()
                stack.pop()
            else:
                while( (len(stack)!=0) and 
                (stack[-1]=='*' or stack[-1]=='.') and 
                (precedence[char]<=precedence[stack[-1]]) 
                ):
                    postfixRegex += stack.pop()
                stack.append(char)
        while len(stack)!=0:
            postfixRegex += stack.pop()
        return postfixRegex

    def makeNFA(self, postfixRegex):
        nfaStack = []
        for char in postfixRegex:
            if self.isAlphabet(char):
                nfaStack.append(self.unitLenRegexToNFA(char))
            elif char=="*":
                nfaStack.append(self.starNFA(nfaStack.pop()))
            elif char=="+":
                NFA2 = nfaStack.pop()
                NFA1 = nfaStack.pop()
                nfaStack.append(self.unionNFA(NFA1,NFA2))
            elif char==".":
                NFA2 = nfaStack.pop()
                NFA1 = nfaStack.pop()
                nfaStack.append(self.concatenationNFA(NFA1,NFA2))
            else:
                print("Literally, an Edge case is there!")
        return nfaStack.pop()

    def convertToNFA(self, regular_expression):
        if regular_expression=="":
            return self.unitLenRegexToNFA('λ')
        
        regular_expression = self.add_dot(regular_expression)
        regular_expression = self.infixToPostfix(regular_expression)
        return self.makeNFA(regular_expression)

# TODO: add a adder class
class RE:
    def __init__(self) -> None:
        self.regex = ''
        self.ready = False
        self.NFA = NFA()

    # TODO: complete this function
    def buildNFAfromRE(self):
        pass

# Run app main
if __name__=='__main__':

    with open('../RE_Input_3.txt', encoding='UTF-8') as file:
        lines = [line.rstrip() for line in file]
        regex = lines[1].strip()
        
        transformer = REtoNFA()
    
        finalNFA = transformer.convertToNFA(regex)
        print(finalNFA)

        alphabet = set()
        for item in finalNFA['alphabet']:
            alphabet.add(item)
        states = {}
        rules = []
        counter = 0
        for item in finalNFA['states']:
            s = 'Q' + str(counter)
            states[s] = item
            counter += 1
        for item in finalNFA['transition_matrix']:
            start_s = set(item[0])
            movement = item[1]
            if movement != 'λ':
                alphabet.add(movement)
            end_s = set(item[2])
            for eqv_s in states:
                if set(states[eqv_s]) == start_s:
                    start_s = eqv_s
                    break
            for eqv_s in states:
                if set(states[eqv_s]) == end_s:
                    end_s = eqv_s
                    break
            rules.append(start_s + ' ' + movement + ' ' + end_s)
            
        start_states = []
        for item in finalNFA['start_states']:
            start_states.append(item)
                
        end_states = []
        for item in finalNFA['terminate_state']:
            end_states.append(item)
                
        string_out = ''
        for item in alphabet:
            string_out += item + ' '
        string_out += '\n'
        for item in states.keys():
            string_out += item + ' '
        string_out += '\n'
        for item in start_states:
            string_out += item + ' '
        string_out += '\n'
        for item in end_states:
            string_out += item + ' '
        string_out += '\n'
        for item in rules:
            string_out += item + '\n'
            
        print(string_out)
        
        with open('out/nfa_res.text', "w+", encoding='UTF-8') as outfile: 
            outfile.write(string_out.strip())
            outfile.close()
        