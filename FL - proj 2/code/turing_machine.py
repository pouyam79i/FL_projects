# this is a turing machine base class to move on a liner tape
class TuringMachine:
    
    def __init__(self, states, initial_states, final_states, transitions) -> None:
        self.states = states
        self.initial_state = initial_states
        self.final_state = final_states
        self.transitions = transitions
    
    # given function
    def run(self, data:str)->str:
        curr_state = self.initial_state
        if len(data) == 0:
            print('null input')
            return ''
        tape = '_' + data + '_'
        print("data in: {} and taped to: ".format(data), end= '')
        print(tape)
        position = 0
        while curr_state != self.final_state:
            try:
                print('flags: cs: {}, pos: {}, tape: {}'.format(curr_state, position, tape), end=' -- ')
                curr_state, movement, write_value = self.transitions[curr_state][tape[position]]
                print('ns: {}, move: {}, write_value: {}'.format(curr_state, movement, write_value))
                # Write on given position 
                tape = tape[:position] + write_value + tape[position+1:]
                if movement == 'L' or movement == 'l':
                    position -= 1
                elif movement == 'R' or movement == 'r':
                    position += 1       
            except:
                print('Turing Machine Failed!')
                return ''
        if tape[0] == '_':
            tape = tape[1:]
        if tape[len(tape)-1] == '_':
            tape = tape[:len(tape)-1]
        print('')
        print('final tape is: ', end='')
        print(tape)
        return tape
