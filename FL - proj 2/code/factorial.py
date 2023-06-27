from turing_machine import TuringMachine
from multiply import Multiply
from time import sleep

class Factorial(TuringMachine):
    def __init__(self) -> None:
        states = ['q0', 'q1', 'q2']
        initial_states = 'q0'
        final_states = 'q2'
        transitions = {
            'q0': {
                '1':('q1','R','x'),
                '_':('q1','R','_')
            },
            'q1':  {
                '1':('q1','R','x'),
                '_':('q2','Halt','_')
            }
        }
        super().__init__(states, initial_states, final_states, transitions)
        
    # given function
    def run(self, data:str)->str:
        curr_state = self.initial_state
        if len(data) == 0:
            # print('null input')
            return ''
        tape = data
        if tape[0] != '_':
            tape = '_' + tape
        if tape[len(tape)-1] != '_':
            tape = tape + '_'
        tape2 = '1'
        result = '_'
        # print("data in: {} and taped to: ".format(data), end= '')
        # print(tape)
        position = 0
        while curr_state != self.final_state:
            try:
                if self.delay > 0:
                    sleep(self.delay)
            except:
                pass
            try:
                # print('flags: cs: {}, pos: {}, tape: {}'.format(curr_state, position, tape), end=' -- ')
                curr_state, movement, write_value = self.transitions[curr_state][tape[position]]
                # print('ns: {}, move: {}, write_value: {}'.format(curr_state, movement, write_value))
                # Write on given position 
                tape = tape[:position] + write_value + tape[position+1:]
                if movement == 'L' or movement == 'l':
                    position -= 1
                elif movement == 'R' or movement == 'r':
                    position += 1    
                if tape[len(tape)-1] != '_':
                    tape = tape + '_'  
                if tape[0] != '_':
                    tape = '_' + tape 
                # simplified turing to read middle answer and write it to output result
                if tape[position] != '1':
                    continue
                mul_tm = Multiply()
                mul_tm.delay = self.delay
                # print('cp: {}'.format(tape[position:len(tape)-1]))
                tape2 = mul_tm.run(tape2 + '#' + tape[position:len(tape)-1] + '#')
                lastHashTah = tape2.rfind('#')
                tape2 = tape2[lastHashTah+1:]
                # print('tape2: {}'.format(tape2)) 
            except:
                # print('Turing Machine Failed!')
                return ''
        tape = tape2
        if tape[0] == '_':
            tape = tape[1:]
        if tape[len(tape)-1] == '_':
            tape = tape[:len(tape)-1]
        # print('')
        # print('final tape is: ', end='')
        # print(tape)
        return tape
