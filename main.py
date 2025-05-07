from time import sleep
from random import randint
from sys import argv
if __name__ == '__main__':
    from TuringMachine import TuringMachine
    tm = TuringMachine()

    tape = []
    for i in range(10):
        tape.append(str(i % 10))

    tm.load_tape(tape)
    print(tm)

    direction = argv[1]
    wait = 0.1

    match (direction):
        case 'ra':
            for i in range(200):
                sleep(wait)
                if randint(0, 1):
                    tm._move('l')
                else:
                    tm._move('r')
                print(tm)
                print(tm.head)
        case 'r':
            for i in range(35):
                sleep(wait)
                tm._move('r')
                print(tm)
                print(tm.head)
        case 'l':
            for i in range(20):
                sleep(wait)
                tm._move('l')
                print(tm)
                print(tm.head)
        case 'b':
            for i in range(100):
                sleep(wait)
                tm._move('l')
                print(tm)
                print(tm.head)

            for i in range(150):
                sleep(wait)
                tm._move('r')
                print(tm)
                print(tm.head)


"""
_______________
| |1| |0| | |&|
‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
"""