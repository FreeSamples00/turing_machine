# Turing Machine

*That’s right, python is officially Turing complete! /s*

## Overview

This is a python implementation of the [Turing Machine](https://en.wikipedia.org/wiki/Turing_machine). It is run in the command line and visualizes the machine’s process via an ASCII display. The machine is fully programmable, taking in both a custom program and a tape input before processing. The machine can hold and infinite\* (\*memory bound) number of states, and can recognize any unicode character\* as an input symbol (\*excluding `*` and `_` which are used for wildcard and blank symbols). Speed and display options can be set

*All the implementation logic is contained in `TuringMachine.py`*

## Command Line interface

The `main.py` file contains a CLI for the machine. Argument options are as follows:

- `-h`: displays help message, does not run anything

- `-p`: the location of a program to load (also accepts the name or number of a program stored in the `./programs` directory)
- `-t`: the tape to process (passed as a string of symbols)
- `-s`: the speed the machine should run at, i.e. how many seconds to wait between instructions (accepts any positive float)
- `--turbo`: enables turbo mode, where speed is uncapped and the display is disabled (helpful for complex programs)

If either the program or tape is left unspecified, the user will be prompted for them. The default speed is 0.15s.

## Programs

Programs are formatted txt files which contain instructions for the machine.

Instructions for a Turing Machine consist of 5 parts:

- The current state of the machine
- The inputted symbol (`*` is a wildcard accepting any symbol, `_` is a blank cell)
- The new symbol to write to tape (`*` indicates no write, `_` indicates a deletion)
- The direction to move the head (`*` indicates no movement, `l` & `r` are left and right respectively)
- The state to switch the machine to (`*` indicates no change)

### Creating a program / syntax

Each program is stored in a `.txt` file. Comments are indicated by `#`. The machine always starts in a ‘start’ state, so transitions away from this state must be created. The program ends with three states: ‘halt’ stops the machine w/ output on the tape, ‘halt-accept’ stops the machine while accepting the input, ‘halt-reject’ stops the machine while rejecting the input. All programs must end in one of these states to avoid an hanging.

Instruction format: 

<current state> <read symbol> <write symbol> <move direction> <new state>

Instruction elements are space-separated, Each instruction is on its own line.

*See `program_template.txt` for help and `./programs` for examples*

### Included Programs

*All credit to [https://morphett.info/turing/turing.html](https://morphett.info/turing/turing.html) for creating these programs* 

There are a few Turing programs included with this project. They were found at the link specified above and translated to my implementation’s syntax. For more information on what they do please go to that site, or check the notes in the program header.

## Notes

The ASCII visualization was tested in the macOS Terminal.app with both even and odd window widths. It is not guaranteed to work on any other system or with any other terminal emulator (although it should).