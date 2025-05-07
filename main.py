from time import sleep
from random import randint
from sys import argv
if __name__ == '__main__':
    from TuringMachine import TuringMachine
    tm = TuringMachine("./programs/binary_palindrome.txt")

    tape = "101001"

    tm.load_tape(tape)

    output = tm.execute_program()

    print(output)
