"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""

from typing import TextIO, Dict


class VMWriter:
    """
    Writes VM commands into a file. Encapsulates the VM command syntax.
    """

    _PUSH_COMMAND = "push"
    _POP_COMMAND = "pop"
    _LABEL_COMMAND = "label"
    _GOTO_COMMAND = "goto"
    _IF_COMMAND = "if-goto"
    _CALL_COMMAND = "call"
    _FUNCTION_COMMAND = "function"
    _RETURN_COMMAND = "return"
    _ARITHMETIC_COMMANDS_SWITCHER: Dict[str, str] = {
        "+": "add",
        "-": "sub",
        "*": "call Math.multiply 2",
        "/": "call Math.divide 2",
        "&": "and",
        "|": "or",
        "<": "lt",
        ">": "gt",
        "=": "eq",
        "~": "neg",
        "^": "shiftLeft",
        "#": "shiftRight"
    }
    _SEGMENT_SWITCHER: Dict[str, str] = {
        "var": "local",
        "field": "this"
    }

    def __init__(self, output_stream: TextIO) -> None:
        """Creates a new file and prepares it for writing VM commands."""
        self._output_file: TextIO = output_stream

    def write_push(self, segment: str, index: int) -> None:
        """
        Writes a VM push command.

        :param segment: The segment to push to.
                        It can be "CONST", "ARG", "LOCAL", "STATIC", "THIS", "THAT", "POINTER" or "TEMP".
        :param index: The index to push to.
        """
        self._output_file.write(f"{self._PUSH_COMMAND} {self._SEGMENT_SWITCHER.get(segment, segment)} {index}\n")

    def write_pop(self, segment: str, index: int) -> None:
        """
        Writes a VM pop command.

        :param segment: The segment to pop from.
                        It can be "CONST", "ARG", "LOCAL", "STATIC", "THIS", "THAT", "POINTER" or "TEMP".
        :param index: The index to pop from.
        """
        self._output_file.write(f"{self._POP_COMMAND} {self._SEGMENT_SWITCHER.get(segment, segment)} {index}\n")

    def write_arithmetic(self, command: str) -> None:
        """
        Writes a VM arithmetic command.

        :param command: The command to write.
                        It can be "+", "-", "=", ">", "<", "&", "|", "~", "^", "#" or "not".
        """
        self._output_file.write(f"{self._ARITHMETIC_COMMANDS_SWITCHER.get(command, command)}\n")

    def write_label(self, label: str) -> None:
        """
        Writes a VM label command.

        :param label: The label to write.
        """
        self._output_file.write(f"{self._LABEL_COMMAND} {label}\n")

    def write_goto(self, label: str) -> None:
        """
        Writes a VM goto command.

        :param label: The label to go to.
        """
        self._output_file.write(f"{self._GOTO_COMMAND} {label}\n")

    def write_if(self, label: str) -> None:
        """
        Writes a VM if-goto command.

        :param label: The label to go to.
        """
        self._output_file.write(f"{self._IF_COMMAND} {label}\n")

    def write_call(self, name: str, n_args: int) -> None:
        """
        Writes a VM call command.

        :param name: The name of the function to call.
        :param n_args: The number of arguments the function receives.
        """
        self._output_file.write(f"{self._CALL_COMMAND} {name} {n_args}\n")

    def write_function(self, name: str, n_locals: int) -> None:
        """
        Writes a VM function command.

        :param name: The name of the function.
        :param n_locals: The number of local variables the function uses.
        """
        self._output_file.write(f"{self._FUNCTION_COMMAND} {name} {n_locals}\n")

    def write_return(self) -> None:
        """Writes a VM return command."""
        self._output_file.write(f"{self._RETURN_COMMAND}\n")
