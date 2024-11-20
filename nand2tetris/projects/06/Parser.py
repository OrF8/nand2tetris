"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
from typing import List, TextIO, Dict
import bigvars
from Code import Code

# Represents the index of the current available variable.
# According to the specs, the first variable is stored at memory location 16.
VARIABLE_IDX = 16


def remove_whitespace_and_comments(lines: List[str]) -> List[str]:
    """
    Removes all whitespace and comments from a line.

    Args:
        lines (List[str]): A list of lines to remove whitespace and comments from.

    Returns:
        List[str]: A list of lines without whitespace and comments.
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
        line = ''.join(line.split())  # Remove all whitespace characters
        result.append(line)
    return result


class Parser:
    """
    Encapsulates access to the input code. Reads an assembly program
    by reading each command line-by-line, parses the current command,
    and provides convenient access to the commands components (fields
    and symbols). In addition, removes all white space and comments.
    """

    def __init__(self, input_file: TextIO) -> None:
        """
        Opens the input file and gets ready to parse it.

        :argument:
            input_file (TextIO): input file.
        """
        # A good place to start is to read all the lines of the input:
        self.input_lines: List[str] = remove_whitespace_and_comments(input_file.read().splitlines())
        self.current_command_idx: int = -1
        self.current_index_wo_labels: int = -1
        self.current_command: str = ''
        self.symbol_table: Dict[str, int] = bigvars.SYMBOL_TABLE.copy()

    def has_more_commands(self) -> bool:
        """
        Are there more commands in the input?

        :return:
            bool: True if there are more commands, False otherwise.
        """
        return self.current_command_idx < len(self.input_lines) - 1

    def advance(self, l_comm: bool = False) -> None:
        """
        Reads the next command from the input and makes it the current command.
        Should be called only if has_more_commands() is true.

        :argument:
            l_comm (bool): a boolean value to check if the current command is an L_COMMAND.
        """
        if not l_comm:
            self.current_index_wo_labels += 1
        self.current_command_idx += 1
        self.current_command = self.input_lines[self.current_command_idx]

    def command_type(self) -> str:
        """
        :return:
            str: the type of the current command:
                "A_COMMAND" for @Xxx where Xxx is either a symbol or a decimal number
                "C_COMMAND" for dest=comp;jump
                "L_COMMAND" (actually, pseudo-command) for (Xxx) where Xxx is a symbol
        """
        if self.current_command.startswith("@"):
            return "A_COMMAND"
        if self.current_command.startswith("("):
            return "L_COMMAND"
        return "C_COMMAND"

    def symbol(self) -> str:
        """
        :return:
            str: the symbol Xxx of the current command @Xxx or
                (Xxx). Should be called only when command_type() is "A_COMMAND" or
                "L_COMMAND".
        """
        return self.current_command.strip("()@")  # Remove the parentheses and @

    def dest(self) -> str:
        """
        :return:
            str: the dest mnemonic in the current C-command. Should be called 
                 only when commandType() is "C_COMMAND".
        """
        if (idx := self.current_command.find("=")) == -1:
            return ""
        return self.current_command[:idx]

    def comp(self) -> str:
        """
        :return:
            str: the comp mnemonic in the current C-command. Should be called 
                 only when commandType() is "C_COMMAND".
        """
        idx = 0
        if (og_idx := self.current_command.find("=")) == -1:
            idx = 0
        if (end_idx := self.current_command.find(";")) == -1:
            end_idx = len(self.current_command)
        return self.current_command[idx:end_idx] if og_idx == -1 else self.current_command[og_idx + 1:end_idx]

    def jump(self) -> str:
        """
        :return:
            str: the jump mnemonic in the current C-command. Should be called 
                 only when commandType() is "C_COMMAND".
        """
        if (idx := self.current_command.find(";")) == -1:
            return ""
        return self.current_command[idx + 1:]

    def first_pass(self) -> None:
        """
        First pass of the assembler, which adds all labels to the symbol table.
        """
        l_comm: bool = False
        while self.has_more_commands():
            self.advance(l_comm)
            if self.command_type() == "L_COMMAND":
                l_comm = True
                self.symbol_table[self.symbol()] = self.current_index_wo_labels
            else:
                l_comm = False
        self.current_command_idx = -1
        self.current_command = ''

    def second_pass(self) -> None:
        """
        Second pass of the assembler, which adds all variables to the symbol table.
        """
        global VARIABLE_IDX
        while self.has_more_commands():
            self.advance()
            if self.command_type() == "A_COMMAND":
                symbol = self.symbol()
                if symbol not in self.symbol_table:
                    if not symbol.isnumeric():
                        self.symbol_table[symbol] = VARIABLE_IDX
                        VARIABLE_IDX += 1
                    else:
                        self.symbol_table[symbol] = int(self.symbol())
        self.current_command_idx = -1
        self.current_command = ''

    def is_extended_c_command(self) -> bool:
        """
        Checks if the current C-command is an extended C-command.

        :return:
            bool: True if the current C-command is an extended C-command, False otherwise.
        """
        return "<<" in self.current_command or ">>" in self.current_command

    def code(self) -> List[str]:
        """
        Converts the commands into binary code.
        :return:
            List[str]: a list of binary code strings.
        """
        result: List[str] = []
        while self.has_more_commands():
            self.advance()
            if self.command_type() == "A_COMMAND":
                result.append(f"0{self.symbol_table[self.symbol()]:015b}")
            elif self.command_type() == "C_COMMAND":
                if self.is_extended_c_command():
                    result.append(f"101{Code.comp(self.comp(), True)}"
                                  f"{Code.dest(self.dest())}{Code.jump(self.jump())}")
                else:
                    result.append(f"111{Code.comp(self.comp())}{Code.dest(self.dest())}{Code.jump(self.jump())}")
        return result
