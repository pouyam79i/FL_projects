# This is a Turing Machine to calculate below function
# f(n) = (3n+1)!

class TuringMachine:
    
    def __init__(self) -> None:
        pass
    
    # given function
    def function(n: int) -> bool:
        pass
    
# Run app main
if __name__ == "__main__":
    tn = TuringMachine()
    n = input('Give me the n required for function:')
    try:
        tn.function(int(n))
    except:
        print('Function failed to operate!')
    