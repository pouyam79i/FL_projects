from add_one import AddOne
from multiply import Multiply
from factorial import Factorial
# main functionality
def main(X:str):
    # print('start')
    mul_by_3_TM = Multiply()
    res1 = mul_by_3_TM.run(X+"#"+'111'+'#')
    lastH = res1.rfind('#')
    res1 = res1[lastH+1:]
    # # print('res1: {}'.format(res1))
    add_one_TM = AddOne()
    res2 = add_one_TM.run(res1)
    # # print('res2: {}'.format(res2))
    factorial_TM = Factorial()
    final_res = factorial_TM.run(res2)
    # print('')
    # print('')
    # print('')
    # Final result is equal to number of ones exist in last res in DEC
    print('Final Result in decimal: {}'.format(len(final_res)))
    
# Run app main
if __name__ == "__main__":
    # running main
    main(input('please input a unary number greater than zero using only {1}:'))
