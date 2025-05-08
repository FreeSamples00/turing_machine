from time import sleep
from os import get_terminal_size

class Instruction:
    """Class to hold instruction information"""

    def __init__(self):
        self.curr_state = None
        self.input = None
        self.write_symbol = None
        self.move_direction = None
        self.new_state = None

    def __str__(self):
        return f"{self.curr_state} {self.input} {self.write_symbol} {self.move_direction} {self.new_state}"

class TuringMachine:
    """Turing machine implementation. One tape, one head, customizable programming, infinite tape."""

    # ========================== CLASS CONSTANTS ==========================

    # built-in symbols and states
    _BLANK = "_"
    _HALTS = ('halt-accept', 'halt-reject', 'halt')
    _START = 'start'
    _WILDCARD = '*'

    # ========================== DUNDER METHODS ==========================

    def __init__(self, program_path: str=None, tape = None):
        """Initialize blank turing machine
        Args:
            filepath (str): path to program to load (optional)
            tape (str or list[str]): tape to load (optional)
        """

        # private variables
        self._alphabet = {'*', '_'} # default symbols 
        self._states = {            # default states
            'start',
            'halt-accept',
            'halt-reject'
            }
        self._cycle_count = 0       # set cycle count to zero

        # public variables
        self.head = 1               # initialize head location
        self.state = self._START    # initialize state to 'start'
        self.tape = None            # initialize blank tape
        self.complete = False       # set complete flag to true
        self.instruction_set = None # initialize instruction

        # initializations
        if program_path is not None:
            self.load_program(program_path)

        if tape is not None:
            self.load_tape(tape)

    def __str__(self) -> str:
        """Generate visual output of turing machine (head + tape), size bound to terminal window"""

        # static variables
        HEAD_COLOR = 33
        HEAD1 = f"\033[{HEAD_COLOR}m\u25bc\033[0m" # colored down triangle
        HEAD2 = f"\033[{HEAD_COLOR}m\u25b2\033[0m" # colored up triangle

        # get terminal width
        try:
            width = get_terminal_size()[0]
        except:
            width = 100

        # create pads
        head_pad = width // 2
        tape_pad = head_pad - self.head * 2
        if tape_pad % 2 == 0: # off by one fix if terminal is an odd width
            tape_pad -= 1

        # calculate width of tape (used for top and bottom lines)
        tape_width = len(self.tape)*2 + 1

        # calculate bounds to apply to output string
        left_bound = max(self.head * 2 - head_pad + 1, 0)
        right_bound = left_bound + width

        # format status indicators
        state_str = f"State: {self.state}"
        cycles_str = f"Cycles: {self._cycle_count}"
        offset = 0 # offset to account for formatting math w/ escape codes

        # colorize state if in halt state
        if self.state == 'halt-accept':
            state_str = state_str[:6] + " \033[92mACCEPTED\033[0m"
            offset = 9
        elif self.state == 'halt-reject':
            state_str = state_str[:6] + " \033[91mREJECTED\033[0m"
            offset = 9
        elif self.state == 'halt':
            state_str = state_str[:6] + " \033[93mCOMPLETE\033[0m"
            offset = 9

        # create head icons and info
        head_1 = f"{state_str:<{head_pad+offset}}{HEAD1}\n"
        head_2 = f"{cycles_str:<{head_pad}}{HEAD2}"
    

        # create separated cells to place in tape
        tape = self.tape.copy()
        for i in range(len(tape)): # replace blank symbol with space
            if tape[i] == self._BLANK:
                tape[i] = ' '
        tape_2 = f"{" "*tape_pad}|{"|".join(tape)}|"[left_bound:right_bound] + "\n"

        # place top and bottom tape lines
        tape_1 = f"{" "*tape_pad}{"_"*tape_width}"[left_bound:right_bound] + "\n"
        tape_3 = f"{" "*tape_pad}{"‾"*tape_width}"[left_bound:right_bound] + "\n"

        # return final output (plus ANSI escape code to clear terminal)
        return "\033c" + head_1 + tape_1 + tape_2 + tape_3 + head_2

    # ========================== PRIVATE METHODS ==========================

    def _move(self, dir: str) -> None:
        """Move head by one
        Args:
            dir (str): Direction to move. 'r': right, 'l': left, '*': no move
        """
        match (dir.lower()):
            case 'r': # move head to the right
                self.head +=1
                if self.head >= len(self.tape): # grow tape if needed
                    self.tape.append(self._BLANK)
            case 'l': # move head to the left
                self.head -= 1
                if self.head < 0: # grow tape if needed
                    self.head += 1
                    self.tape.insert(0, self._BLANK)
            case self._WILDCARD: # do not move head
                return
            case _:
                raise ValueError(f"'{dir}' not a valid movement direction.")
            
    def _read(self) -> str:
        """Read head-pointed cell"""
        assert 0 <= self.head < len(self.tape), f"Head: {self.head} outside of tape"
        return str(self.tape[self.head])
    
    def _write(self, symbol: str) -> None:
        """Write symbol to head-pointed cell
        Args:
            symbol (str): one character symbol to write, '*' will write nothing
        """
        assert 0 <= self.head < len(self.tape), f"Head: {self.head} outside of tape"
        assert len(symbol) == 1, f"len({symbol} != 1"
        if symbol != self._WILDCARD:
            self.tape[self.head] = symbol

    def _set_state(self, state: str):
        """Set machine state"""
        if state != self._WILDCARD:
            self.state = state

    def _get_instruction(self, state: str, input: str) -> Instruction:
        """Gets an instruction from program
        Args:
            state (str): current state
            input (str): input symbol
        Returns:
            Instruction: Instruction object
        """
        normal = f"{state}:{input}"
        wildcard1 = f"{state}:{self._WILDCARD}"
        wildcard2 = f"{self._WILDCARD}:{state}"
        wildcard3 = f"{self._WILDCARD}:{self._WILDCARD}"

        for key in (normal, wildcard1, wildcard2, wildcard3):
            if key in self.instruction_set:
                return self.instruction_set[key]
            
        print(f"\033[91mERROR: state: '{state}', input: '{input}' not found in program.\033[0m")
        exit()
    
    # ========================== PUBLIC METHODS ==========================
    
    def load_program(self, filepath: str) -> None:
        """Load instruction set into machine
        Args:
            filepath (str): path to a csv formatted file containing instruction set information
        """
        assert self.instruction_set is None, "Cannot reload instructions without first resetting"

        try:
            file = open(filepath)
        except:
            raise ValueError(f"File {filepath} not found.")
        
        line_counter = 0
        self.instruction_set = {}
        
        inst: Instruction
        for line in file.readlines():
            line_counter += 1
            line = line.strip()
            try:
                if (len(line) == 0) or (line[0] == "#"):
                    continue
                if '#' in line:
                    line = line[:line.index('#')]
            except:
                raise ValueError(f"Error in comment processing on line {line_counter} of {filepath}")
            args = line.split(" ")
            inst = Instruction()

            try: # read curr_state
                inst.curr_state = args[0]
                self._states.add(inst.curr_state)
            except:
                raise ValueError(f"Error parsing <curr_state> on line {line_counter} of {filepath}")
            
            try: # read input
                assert len(args[1]) == 1, f"Arg {args[1]} on line {line_counter} of {filepath} is invalid"
                inst.input = args[1]
                self._alphabet.add(inst.input)
            except:
                raise ValueError(f"Error parsing <input> on line {line_counter} of {filepath}")
            
            try: # read write_symbol
                assert len(args[1]) == 1, f"Arg {args[1]} on line {line_counter} of {filepath} is invalid"
                inst.write_symbol = args[2]
                self._alphabet.add(inst.write_symbol)
            except:
                raise ValueError(f"Error parsing <write_symbol> on line {line_counter} of {filepath}")
            
            try: # read move_direction
                assert len(args[1]) == 1, f"Arg {args[1]} on line {line_counter} of {filepath} is invalid"
                inst.move_direction = args[3]
            except:
                raise ValueError(f"Error parsing <move_direction> on line {line_counter} of {filepath}")
            
            try: # read new_state
                inst.new_state = args[4]
                self._states.add(inst.new_state)
            except:
                raise ValueError(f"Error parsing <new_state> on line {line_counter} of {filepath}")
            
            self.instruction_set[str(f"{inst.curr_state}:{inst.input}")] = inst


    def load_tape(self, input) -> None:
        """Load input onto tape
        Args:
            input: str or list of symbols to transfer to tape
        """
        assert self.tape is None, "Cannot reload tape without first resetting"
        self.tape = []

        # load string into tape
        if type(input) is str:
            input = "_" + input + "_"
            for sym in input:
                assert len(sym) == 1, f"'{sym}' is not a valid symbol"
                if sym == ' ': # translate whitespace
                    self.tape.append(self._BLANK)
                else:
                    self.tape.append(sym)

        # load list into tape
        elif type(input) is list:
            self.tape.append(self._BLANK)
            for sym in input:
                assert len(sym) == 1, f"'{sym}' is not a valid symbol"
                if sym == ' ': # translate whitespace
                    self.tape.append(self._BLANK)
                else:
                    self.tape.append(str(sym))
            self.tape.append(self._BLANK)
        else:
            raise TypeError(f"input type '{type(input)}' is invalid")

    def cycle(self, display: bool=True) -> None:
        """Execute one instruction cycle
        Args:
            display (bool): toggles printing of turing machine (default is True)
        """
        assert not self.complete, "Cannot execute while machine is complete"
        assert self.tape is not None, "Cannot execute while tape unloaded"
        assert self.instruction_set is not None, "Cannot execute while instruction set unloaded"

        # cycle logic:  read, change state, write, move
        input = self._read()
        inst = self._get_instruction(self.state, input)
        self._set_state(inst.new_state)
        self._write(inst.write_symbol)
        self._move(inst.move_direction)

        # if halt state reached change status
        if self.state in self._HALTS:
            self.complete = True
        
        self._cycle_count += 1

        if display:
            print(self)

    def execute_program(self, speed: float=0.15, display: bool=True):
        """Execute instruction cycles until reaching a HALT state.
        Args:
            speed (float): time delay between cycles in seconds (default is 0.15)
            display (bool): whether or not to display turing machine while running (default is True)
        """
        if display:
            print(self)

        # while not halted, execute cycles on delay
        while not self.complete:
            sleep(speed)
            self.cycle(display=display)
    
    def get_result(self) -> tuple[bool, list[str]]:
        """Get result from machine.
        Returns:
            (accept/reject, tape): accept status, and list of tape elements
        """
        assert self.complete, f"get_result() called while machine is not complete"

        # convert tape to string
        tape = ""
        for sym in self.tape:
            if sym == '_':
                tape += ' '
            else:
                tape += sym
        tape = tape.strip()

        # return state of machine
        if self.state == 'halt-accept':
            return True, tape
        elif self.state == 'halt-reject':
            return False, tape
        else:
            return None, tape
        
    def reset(self, hard: bool=False) -> None:
        """Reset machine for another execution
        Args:
            hard (bool): if true also clears instruction set (defaults to false)
        """

        # reset operating variables
        self.head = 1
        self.complete = False
        self.tape = None
        self._cycle_count = 0
        self.state = self._START

        # if specified, fully reset machine
        if hard:
            self.instruction_set = None
            self._alphabet = {'*', '_'}
            self._states = {'start', 'halt-accept', 'halt-reject'}
        

# TODO: write more programs
# TODO: create README