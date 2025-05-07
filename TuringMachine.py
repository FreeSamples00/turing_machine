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
        # ret_val = ""
        # ret_val += f"Instruction: \033[90mstate: \033[96m{self.curr_state}\033[0m  "
        # ret_val += f"\033[90minput: \033[96m{self.input}\033[0m  "
        # ret_val += f"\033[90mwrite: \033[96m{self.write_symbol}\033[0m  "
        # ret_val += f"\033[90mdirection: \033[96m{self.move_direction}\033[0m  "
        # ret_val == f"\033[90mnew state: \033[96m{self.new_state}\033[0m  "
        # return ret_val
        return f"{self.curr_state} {self.input} {self.write_symbol} {self.move_direction} {self.new_state}"

class TuringMachine:
    """Turing machine implementation. One tape, one head, customizable programming, infinite tape."""

    # built-in symbols and states
    _BLANK = "_"
    _HALTS = ('halt-accept', 'halt-reject')
    _START = 'start'

    def __init__(self, filepath: str):
        """Initialize blank turing machine
        Args:
            filepath (str): path to turing program
        """
        self.head = 1               # initialize head location
        self.state = self._START    # initialize state to 'start'
        self.tape = []              # initialize blank tape
        self.active = True          # set active (not halted) flage to true
        self.instruction_set = {}   # initialize instruction set dict (will contains dicts of instructions based on state)
        self._load_instruction_set(filepath)

    def _move(self, dir: str) -> None:
        """Move head by one
        Args:
            dir (str): Direction to move. 'r': right, 'l': left, '*': no move
        """
        match (dir.lower()):
            case 'r':
                self.head +=1
                if self.head >= len(self.tape): # grow tape if needed
                    self.tape.append(self._BLANK)
            case 'l':
                self.head -= 1
                if self.head < 0: # grow tape if needed
                    self.head += 1
                    self.tape.insert(0, self._BLANK)
            case '*':
                return
            case _:
                raise ValueError(f"'{dir}' not a valid movement direction.")
            
    def _read(self) -> str:
        """Read current cell"""
        assert 0 <= self.head < len(self.tape), f"Head: {self.head} outside of tape"
        return str(self.tape[self.head])
    
    def _write(self, symbol: str) -> None:
        assert 0 <= self.head < len(self.tape), f"Head: {self.head} outside of tape"
        assert len(symbol) == 1, f"len({symbol} != 1"
        if symbol != '*':
            self.tape[self.head] = symbol

    def _set_state(self, state: str):
        """Set machine state"""
        if state != '*':
            self.state = state

    def _load_instruction_set(self, filepath: str) -> None:
        """Load instruction set into machine
        Args:
            filepath (str): path to a csv formatted file containing instruction set information
        """
        try:
            file = open(filepath)
        except:
            raise ValueError(f"File {filepath} not found.")
        
        inst: Instruction
        for line in file.readlines():
            line = line.strip()
            if (len(line) == 0) or (line[0] == "#"):
                continue
            if '#' in line:
                line = line[line.index('#'):]
            args = line.split(" ")
            inst = Instruction()
            inst.curr_state = args[0]
            inst.input = args[1]
            inst.write_symbol = args[2]
            inst.move_direction = args[3]
            inst.new_state = args[4]
            self.instruction_set[str(f"{inst.curr_state}:{inst.input}")] = inst

    def _get_instruction(self, state: str, input: str) -> Instruction:
        """Gets an instruction from program
        Args:
            state (str): current state
            input (str): input symbol
        Returns:
            Instruction: Instruction object
        """
        normal = f"{state}:{input}"
        wildcard1 = f"{state}:*"
        wildcard2 = f"*:{state}"
        wildcard3 = f"*:*"

        for key in (normal, wildcard1, wildcard2, wildcard3):
            if key in self.instruction_set:
                return self.instruction_set[key]
            
        raise ValueError(f"[{state}, {input}] not in instruction set")

    def load_tape(self, input) -> None:
        """Load input onto tape
        Args:
            input: str or list of symbols to transfer to tape
        """
        if type(input) is str:
            input = "_" + input + "_"
            for sym in input:
                if len(sym) != 1:
                    raise ValueError(f"'{sym}' is not a valid symbol")
                self.tape.append(sym)

        elif type(input) is list:
            self.tape.append(self._BLANK)
            for sym in input:
                if len(str(sym)) != 1:
                    raise ValueError(f"'{sym}' is not a valid symbol")
                self.tape.append(str(sym))
            self.tape.append(self._BLANK)
        else:
            raise TypeError(f"input type '{type(input)}' is invalid")

    def cycle(self, display: bool=True) -> None:
        """Execute one instruction cycle
        Args:
            display (bool): toggles printing of turing machine (default is True)
        """
        # implement cycle logic:  read, change state, write, move
        input = self._read()
        inst = self._get_instruction(self.state, input)
        self._set_state(inst.new_state)
        self._write(inst.write_symbol)
        self._move(inst.move_direction)

        if self.state in self._HALTS:
            self.active = False

        if display:
            print(self)

    def execute_program(self, speed: float=0.15) -> tuple[bool, list[str]]:
        """Execute instruction cycles until reaching a HALT state.
        Args:
            speed (float): time (seconds) in between clock cycles
        Returns:
            (accept/reject, tape): accept status, and list of tape elements
        """

        # TODO: also print state and other information
        
        # while not halted, execute cycles on delay
        while self.active:
            sleep(speed)
            self.cycle()

        return self.state, self.tape

    def __str__(self) -> str:
        """Generate visual output of turing machine (head + tape), size bound to terminal window"""

        # static variables
        _HEAD_COLOR = 33
        _HEAD1 = f"\033[{_HEAD_COLOR}m\u25bc\033[0m"
        _HEAD2 = f"\033[{_HEAD_COLOR}m\u25b2\033[0m"

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
        
        # place head icons
        head_1 = f"{" "*head_pad}{_HEAD1}\n"
        head_2 = f"{" "*head_pad}{_HEAD2}"

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
    

# TODO: write more programs
# TODO: create README
# TODO: create git repo