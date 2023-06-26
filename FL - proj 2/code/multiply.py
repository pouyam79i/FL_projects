from turing_machine import TuringMachine

class Multiply(TuringMachine):
    def __init__(self) -> None:
        states = ['q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6']
        initial_states = 'q0'
        final_states = 'q6'
        transitions = {
            'q0':{
                '_':('q0','R','_'),
                '1':('q1','R','x'),
                '#':('q6','Halt','#')
            },
            'q1':{
                '1':('q1','R','1'),
                '#':('q2','R','#')
            },
            'q2':{
                '1':('q3','R','x'),
                '#':('q5','L','#')
            },
            'q3':{
                '#':('q3','R','#'),
                '1':('q3','R','1'),
                '_':('q4','L','1')
            },
            'q4':{
                '1':('q4','L','1'),
                '#':('q4','L','#'),
                'x':('q2','R','1')
            },
            'q5':{
                '1':('q5','L','1'),
                '#':('q5','L','#'),
                'x':('q0','R','1')
            }
        }
        super().__init__(states, initial_states, final_states, transitions)
        
