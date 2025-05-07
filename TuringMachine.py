from time import sleep
from os import get_terminal_size

class Instruction:

    # def __init__(self, )
    pass

class TuringMachine:
    """Turing machine implementation. One tape, one head, customizable programming, infinite tape."""

    _BLANK = "_"
    _HALTS = ('halt-accept', 'halt-reject')

    def __init__(self):
        """Initialize blank turing machine"""
        self.head = 0 # TODO: where does head start?
        self.state = None
        self.tape = []
        self.instruction_set = {}

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
        # TODO: check if head out of list? do something about it?
        return self.tape[self.head]

    def load_instruction_set(self, filepath: str) -> None:
        """Load instruction set into machine
        Args:
            filepath (str): path to a csv formatted file containing instruction set information
        """
        # TODO: finish load
        # load file
        # interpret file into internal structs
        # dict of states leads to dict of transformation options

        # default accept / reject / start states

        pass

    def load_tape(self, input: list[str]) -> None:
        """Load input onto tape
        Args:
            input (list[str]): list of symbols to transfer onto tape
        """
        # TODO: read tape input and place on tape
        # Add extra blanks on each end of tape

        self.tape.append(self._BLANK)
        for sym in input:
            if len(str(sym)) != 1:
                raise ValueError(f"'{sym}' is not a valid symbol")
            self.tape.append(str(sym))
        self.tape.append(self._BLANK)

    def cycle(self) -> None:
        """Execute one instruction cycle"""
        # TODO: implement cycle logic (read, change state, write, move)
        pass

    def execute_program(self, speed: float=0.25) -> list[str]:
        """Execute instruction cycles until reaching HALT state.
        Args:
            speed (float): time (seconds) in between clock cycles
        """
        # TODO: execute cycles with time delay
        pass

    def __str__(self) -> str:
        _HEAD_COLOR = 33
        _HEAD1 = f"\033[{_HEAD_COLOR}m\u25bc\033[0m"
        _HEAD2 = f"\033[{_HEAD_COLOR}m\u25b2\033[0m"
        width = get_terminal_size()[0]
        head_pad = width // 2
        tape_pad = head_pad - self.head * 2
        if tape_pad % 2 == 0:
            tape_pad -= 1
        tape_width = len(self.tape)*2 + 1
        left_bound = max(self.head * 2 - head_pad + 1, 0)
        right_bound = left_bound + width

        # print("\033c", end="")  # ANSI escape sequence to clear screen
        
        head_1 = f"{" "*head_pad}{_HEAD1}\n"
        head_2 = f"{" "*head_pad}{_HEAD2}\n"

        tape_2 = f"{" "*tape_pad}|{"|".join(self.tape)}|"[left_bound:right_bound] + "\n"
        tape_1 = f"{" "*tape_pad}{"_"*tape_width}"[left_bound:right_bound] + "\n"
        tape_3 = f"{" "*tape_pad}{"‾"*tape_width}"[left_bound:right_bound] + "\n"

        return "\033c" + head_1 + tape_1 + tape_2 + tape_3 + head_2

        
