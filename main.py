from sys import argv
from TuringMachine import TuringMachine

if __name__ == '__main__':
    
    # TODO: choose from programs

    tm = TuringMachine("./programs/binary_palindrome.txt")

    try:
        tape = argv[1]
    except:
        tape = "_"

    tm.load_tape(tape)

    tm.execute_program()

    print(tm.get_result())