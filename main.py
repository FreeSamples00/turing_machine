from TuringMachine import TuringMachine
from os import listdir
from sys import argv
from time import sleep

if __name__ == '__main__':

    SPEED = 0.15
    DISPLAY = True
    TURBO = False

    # TODO: accept turbo mode from CLI?

    print("\033c", end="") # clear terminal

    # find programs files
    programs = sorted(listdir("./programs/"))
   
    # get user input to load program
    if len(argv) > 1 and argv[1].isdigit():
        choice = argv[1]
        print(f"Program: {programs[int(choice)][:-4]}\n")
    else:
        choice = ""
        print("======== Choose Program ========\n")
        for i in range(len(programs)):
            print(f"{i}) {programs[i][:-3]}")
        print()
        while (not choice.isdigit()) or (int(choice) >= len(programs)):
            choice = input("Program: ")

    PROGRAM = "./programs/"+programs[int(choice)]
    if programs[int(choice)] == 'primality.txt':
        SPEED = 0.025

    # init machine and load program
    tm = TuringMachine(PROGRAM)

    # get tape from input
    if len(argv) > 2:
        TAPE = argv[2]
        print(f"Tape: {TAPE}\n")
    else:
        TAPE = input("Enter tape: ")

    if len(argv) > 2:
        sleep(1)

    # load tape
    tm.load_tape(TAPE)

    # turbo mode
    if TURBO: 
        SPEED = 0
        DISPLAY = False
    
    # exectute program
    tm.execute_program(speed=SPEED, display=DISPLAY)

    if TURBO:
        print(tm)
