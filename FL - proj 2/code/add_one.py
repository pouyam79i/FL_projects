from turing_machine import TuringMachine

# add one Turing Machine adds 1 to given input (input > 0 and E Z) 
class AddOne(TuringMachine):
    def __init__(self) -> None:
        states = ['q0','q1', 'q2']
        initial_states = 'q0'
        final_states = 'q2'
        transitions = {
            'q0':{'_':('q1', 'R', '_')},
            'q1':{'_':('q2','Halt','1'), '1':('q1', 'R', '1')}
        }
        super().__init__(states, initial_states, final_states, transitions)
