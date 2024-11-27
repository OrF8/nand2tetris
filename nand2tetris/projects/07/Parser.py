"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
from typing import TextIO, List
from MapVars import COMMAND_MAP


class Parser:
    """
    # Parser
    
    Handles the parsing of a single .vm file, and encapsulates access to the
    input code. It reads VM commands, parses them, and provides convenient 
    access to their components. 
    In addition, it removes all white space and comments.

    API:
        - has_more_commands(): bool, True if there are more commands in the input, False otherwise
        - advance(): None, Advances the parser to the next command
        - command_type(): str, The type of the current VM command
        - arg1(): str, The first argument of the current command
        - arg2(): int, The second argument of the current command

    ## `VM Language Specification`

    A .vm file is a stream of characters. If the file represents a
    valid program, it can be translated into a stream of valid assembly 
    commands. VM commands may be separated by an arbitrary number of whitespace
    characters and comments, which are ignored. Comments begin with "//" and
    last until the line's end.
    The different parts of each VM command may also be separated by an arbitrary
    number of non-newline whitespace characters.

    - Arithmetic commands:
      - add, sub, and, or, eq, gt, lt
      - neg, not, shiftleft, shiftright
    - Memory segment manipulation:
      - push <segment> <number>
      - pop <segment that is not constant> <number>
      - <segment> can be any of: argument, local, static, constant, this, that, 
                                 pointer, temp
    - Branching (only relevant for project 8):
      - label <label-name>
      - if-goto <label-name>
      - goto <label-name>
      - <label-name> can be any combination of non-whitespace characters.
    - Functions (only relevant for project 8):
      - call <function-name> <n-args>
      - function <function-name> <n-vars>
      - return
    """

    @staticmethod
    def _remove_whitespace_and_comments(lines: List[str]) -> List[str]:
        """
        Removes all whitespace and comments from the given lines.
        :param lines: The lines to process.
        :return: The processed lines.
        """
        result: List[str] = []
        for line in lines:
            if not line:  # i.e., if the line is empty
                continue
            line = line.strip()
            if not line or line.startswith("//"):  # i.e., if the line is empty or a comment
                continue
            if "//" in line:  # i.e., if the line has a comment
                line = line[:line.index("//")]
            line = ' '.join(line.split())  # Remove all whitespace characters
            result.append(line)
        return result

    def __init__(self, input_file: TextIO) -> None:
        """
        Gets ready to parse the input file.
        :param input_file (TextIO): The input file.
        """
        self._input_lines: List[str] = self._remove_whitespace_and_comments(input_file.read().splitlines())
        self._current_command_idx: int = -1
        self._current_command: str = ''

    def has_more_commands(self) -> bool:
        """
        :return: True if there are more commands in the input, False otherwise.
        """
        return self._current_command_idx < len(self._input_lines) - 1

    def advance(self) -> None:
        """
        Advances the parser to the next command.
        Called only if has_more_commands() is True. Initially, there is no current command.
        """
        self._current_command_idx += 1
        self._current_command = self._input_lines[self._current_command_idx]

    def command_type(self) -> str:
        """
        :return: The type of the current VM command:
                 "C_ARITHMETIC" for all arithmetic commands,
                 "C_PUSH" for push commands,
                 "C_POP" for pop commands,
                 "C_LABEL" for label commands,
                 "C_GOTO" for goto commands,
                 "C_IF" for if-goto commands,
                 "C_FUNCTION" for function commands,
                 "C_RETURN" for return commands,
                 "C_CALL" for call commands.
        """
        return COMMAND_MAP[self._current_command.split()[0]]

    def arg1(self) -> str:
        """
        :return: The first argument of the current command.
                 In case of "C_ARITHMETIC", the command itself (add, sub, etc.) is returned.
                 Should not be called if the current command is "C_RETURN".
        """
        if self.command_type() == "C_ARITHMETIC":
            return self._current_command.split()[0]
        return self._current_command.split()[1]

    def arg2(self) -> int:
        """
        :return: The second argument of the current command.
                 Should be called only if the current command is "C_PUSH", "C_POP", "C_FUNCTION" or "C_CALL".
        """
        return int(self._current_command.split()[2])
