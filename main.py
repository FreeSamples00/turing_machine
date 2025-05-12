from TuringMachine import TuringMachine
from os import listdir
from os.path import exists
from sys import argv

if __name__ == '__main__':

    PROGRAM_DIR = "./programs/"

    # bad input error
    def error(msg: str) -> None:
        print(f"\033[91m{msg}\033[0m")
        exit()

    # attempt to load program options for PROGRAM_DIR
    try:
        programs = sorted(listdir(PROGRAM_DIR))
    except:
        programs = None

    # default settings
    speed = 0.15
    turbo = False

    # input flags
    needs_tape = True
    needs_program = True

    # input variables
    program = None
    tape = None

    # process flags and inputs
    flags = ('--turbo', '-p', '-t', '-s')
    skip = False
    for i in range(len(argv)):
        if not skip:

            # set arg and next_arg
            arg = argv[i]
            try:
                next_arg = argv[i+1]
            except:
                next_arg = None

            # processing logic
            match (arg):

                case '-h': # help message
                    print("\nOptions:")
                    print("-p <string>  \tProgram to load. filepath, ./program name.")
                    print("-t <string>  \tTape to load. string of symbols.")
                    print("-s <float>   \tSpeed. n (float) seconds between instructions.")
                    print("--turbo      \tTurbo mode. Uncapped speed, Does not display.")
                    print("-h           \tThis help message.")
                    exit()
                
                case '--turbo': # set turbo to True
                    turbo = True

                case '-p': # specify program (number or filepath)
                    if next_arg is None or next_arg in flags: error("No program specified")
                    
                    try:
                        program = f"{PROGRAM_DIR}{programs[int(next_arg)]}"
                    except:
                        program = f"{PROGRAM_DIR}{next_arg}.txt"
                        if not exists(program):
                            program = next_arg
                            if not exists(program): error(f"'{next_arg}' not found")

                    skip = True
                    needs_program = False
                
                case '-t': # specify tape input 
                    if next_arg is None or next_arg in flags: error("No tape specified")
                    tape = next_arg
                    needs_tape = False
                    skip = True

                case '-s': # specify the speed
                    if next_arg is None or next_arg in flags: error("No speed specified")
                    try:
                        speed = float(next_arg)
                        if speed < 0:
                            exit()
                    except:
                        error(f"'{next_arg}' not a positive float")
                    skip = True

                case _:
                    if argv.index(arg) > 0: error(f"'{arg}' not valid")

        else:
            skip = False

    # interactive program selection
    if needs_program:
        if programs is None:
            error("No program specified")

        choice = ""
        print("\n======== Choose Program ========\n")
        for i in range(len(programs)):
            print(f"{i}) {programs[i][:-3]}")
        print()
        while (not choice.isdigit()) or (int(choice) >= len(programs)):
            choice = input("Program: ")

        program = f"{PROGRAM_DIR}{programs[int(choice)]}"

    # interactive tape input
    if needs_tape:
        tape = input("\nEnter tape: ")

    # create turing machine
    tm = TuringMachine()

    # load program
    tm.load_program(program)

    # load tape
    tm.load_tape(tape)

    # execute
    if turbo: # turbo mode
        tm.execute_program(display=False, speed=0)
        print(tm)
    else: # normal mode
        tm.execute_program(speed=speed)