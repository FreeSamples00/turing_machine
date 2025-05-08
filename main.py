from TuringMachine import TuringMachine
from os import listdir

if __name__ == '__main__':

    # TODO: clean up code
    # TODO: add a speed recommendation lookup

    print("\033c", end="")

    programs = sorted(listdir("./programs/"))
    choice = ""
    print("Choose program:\n")
    for i in range(len(programs)):
        print(f"{i}) {programs[i][:-3]}")
    print()
    while (not choice.isdigit()) or (int(choice) >= len(programs)):
        choice = input("Program: ")

    PROGRAM = "./programs/"+programs[int(choice)]

    tape = input("Enter tape: ")

    tm = TuringMachine(PROGRAM)

    

    tm.load_tape(tape)
    tm.execute_program()
