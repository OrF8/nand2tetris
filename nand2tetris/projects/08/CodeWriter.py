"""
This _output_stream is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
from typing import TextIO
from MapVars import SEGMENT_MAP


class CodeWriter:
    """
    Translates VM commands into Hack assembly code.

    API:
        - write_arithmetic(command: str) -> None,
                                       Writes the assembly code that is the translation of the given arithmetic command.
        - write_push_pop(command: str, segment: str, index: int) -> None,
                                                  Writes the assembly code that is the translation of the given command.
        - write_label(label: str) -> None, Writes assembly code that affects the label command.
        - write_goto(label: str) -> None, Writes assembly code that affects the goto command.
        - write_if(label: str) -> None, Writes assembly code that affects the if-goto command.
        - write_function(function_name: str, n_vars: int) -> None,
                                                                 Writes assembly code that affects the function command.
        - write_call(function_name: str, n_args: int) -> None, Writes assembly code that affects the call command.
        - write_return() -> None, Writes assembly code that affects the return command.
    """

    _function_call_counter = 0

    def __init__(self, output_stream: TextIO, file_name: str) -> None:
        """
        Initializes the CodeWriter.
        :param output_stream: Output stream.
        """
        self._output_stream = output_stream
        self._file_name = file_name
        self._jmp_index = 0

    def _write_binary_op(self, command: str) -> None:
        """
        Writes the assembly code for binary operations (add, sub, and, or).
        :param command: The binary operation.
        """
        self._output_stream.write("@SP\n")
        self._output_stream.write("AM=M-1\n")
        self._output_stream.write("D=M\n")
        self._output_stream.write("A=A-1\n")
        if command == "add":
            self._output_stream.write("M=M+D\n")
        elif command == "sub":
            self._output_stream.write("M=M-D\n")
        elif command == "and":
            self._output_stream.write("M=M&D\n")
        elif command == "or":
            self._output_stream.write("M=M|D\n")

    def _write_unary_op(self, command: str) -> None:
        """
        Writes the assembly code for unary operations (neg, not, shiftleft, shiftright).
        """
        self._output_stream.write("@SP\n")
        self._output_stream.write("A=M-1\n")
        if command == "neg":
            self._output_stream.write("M=-M\n")
        elif command == "not":
            self._output_stream.write("M=!M\n")
        elif command == "shiftleft":
            self._output_stream.write("M=M<<\n")
        elif command == "shiftright":
            self._output_stream.write("M=M>>\n")

    def _write_comparison(self, command: str) -> None:
        """
        Writes the assembly code for comparison operations (eq, lt, gt).
        """
        self._output_stream.write("@SP\n")
        self._output_stream.write("AM=M-1\n")  # Pop the top value
        self._output_stream.write("D=M\n")    # Store the top value in D
        self._output_stream.write("A=A-1\n")  # Point to the next value
        self._output_stream.write("D=M-D\n")  # Subtract the values

        # Generate labels for true and end
        true_label = f"{self._file_name}.TRUE.{self._jmp_index}"
        end_label = f"{self._file_name}.END.{self._jmp_index}"
        self._jmp_index += 1

        # Write the conditional jump
        self._output_stream.write(f"@{true_label}\n")
        if command == "eq":
            self._output_stream.write("D;JEQ\n")
        elif command == "lt":
            self._output_stream.write("D;JLT\n")
        elif command == "gt":
            self._output_stream.write("D;JGT\n")

        # Write the false case
        self._output_stream.write("@SP\n")
        self._output_stream.write("A=M-1\n")
        self._output_stream.write("M=0\n")  # false: 0
        self._output_stream.write(f"@{end_label}\n")
        self._output_stream.write("0;JMP\n")

        # Write the true case
        self._output_stream.write(f"({true_label})\n")
        self._output_stream.write("@SP\n")
        self._output_stream.write("A=M-1\n")
        self._output_stream.write("M=-1\n")  # true: -1

        # End label
        self._output_stream.write(f"({end_label})\n")

    def write_arithmetic(self, command: str) -> None:
        """
        Writes the assembly code that is the translation of the given arithmetic command.
        For the commands eq, lt, gt, you should correctly
        compare between all numbers our computer supports, and we define the
        value "true" to be -1, and "false" to be 0.
        :param command: The arithmetic command.
        """
        self._output_stream.write(f"// {command}\n")
        if command in {"add", "sub", "and", "or"}:
            self._write_binary_op(command)
        elif command in {"neg", "not", "shiftleft", "shiftright"}:
            self._write_unary_op(command)
        elif command in {"eq", "lt", "gt"}:
            self._write_comparison(command)
        self._output_stream.write("\n")

    def push_stack(self, arg) -> None:
        """
        Pushes the given argument to the stack.
        :param arg: The argument to push.
        """
        self._output_stream.write("@SP\n")
        self._output_stream.write("A = M\n")
        self._output_stream.write(f"M = {arg} \n")
        self._output_stream.write("@SP\n")
        self._output_stream.write("M = M + 1\n")

    def pop_stack(self, segment, index) -> None:
        """
        Pops the top value from the stack and stores it in the given segment and index.
        :param segment: The segment to store the value in.
        :param index: The index in the segment.
        """
        self._output_stream.write(f"@{index}\n")
        self._output_stream.write("D = A\n")
        self._output_stream.write(f"@{SEGMENT_MAP[segment]}\n")
        if (segment == "local") or (segment == "that") or (segment == "this") or (segment == "argument"):
            self._output_stream.write("A=M\n")
        self._output_stream.write("D=A+D\n")
        self._output_stream.write("@R13\n")
        self._output_stream.write("M=D\n")
        self._output_stream.write("@SP\n")
        self._output_stream.write("M=M-1\n")
        self._output_stream.write("A=M\n")
        self._output_stream.write("D=M\n")
        self._output_stream.write("@R13\n")
        self._output_stream.write("A=M\n")
        self._output_stream.write("M=D\n")

    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """
        Writes the assembly code that is the translation of the given command, where command is either C_PUSH or C_POP.
        :param command: The command type (C_PUSH or C_POP).
        :param segment: The memory segment to operate on.
        :param index: The index in the memory segment.
        """
        # Note: each reference to "static i" appearing in the file Xxx.vm should
        # be translated to the assembly symbol "Xxx.i". In the subsequent
        # assembly process, the Hack assembler will allocate these symbolic
        # variables to the RAM, starting at address 16.
        if command == "C_PUSH":
            self._output_stream.write(f"// push {segment} {index}\n")
            if segment in ["temp", "pointer"]:
                self._output_stream.write(f"@{index}\n")
                self._output_stream.write("D=A\n")
                self._output_stream.write(f"@{SEGMENT_MAP[segment]}\n")
                self._output_stream.write("A=A+D\n")
                self._output_stream.write("D=M\n")
                self.push_stack("D")
            elif segment in ["this", "that", "local", "argument"]:
                self._output_stream.write(f"@{index}\n")
                self._output_stream.write("D=A\n")
                self._output_stream.write(f"@{SEGMENT_MAP[segment]}\n")
                self._output_stream.write("A=M+D\n")
                self._output_stream.write("D=M\n")
                self.push_stack("D")
            elif segment == "constant":
                self._output_stream.write(f"@{index}\n")
                self._output_stream.write("D=A\n")
                self.push_stack("D")
            elif segment == "static":
                self._output_stream.write(f"@{self._file_name}.{index}\n")
                self._output_stream.write("D=M\n")
                self.push_stack("D")
        else:
            self._output_stream.write(f"// pop {segment} {index}\n")
            if segment == "static":
                self._output_stream.write("@SP\n")
                self._output_stream.write("AM=M-1\n")
                self._output_stream.write("D=M\n")
                self._output_stream.write(f"@{self._file_name}.{index}\n")
                self._output_stream.write("M=D\n")
            else:
                self.pop_stack(segment, index)
        self._output_stream.write('\n')

    def write_label(self, label: str) -> None:
        """
        Writes assembly code that affects the label command.
        Let "Xxx.foo" be a function within the file Xxx.vm. The handling of
        each "label bar" command within "Xxx.foo" generates and injects the symbol
        "Xxx.foo$bar" into the assembly code stream.
        When translating "goto bar" and "if-goto bar" commands within "foo",
        the label "Xxx.foo$bar" must be used instead of "bar".
        :param label: The label to write.
        """
        self._output_stream.write(f"// label {label}\n")
        self._output_stream.write(f"({label})\n\n")

    def write_goto(self, label: str) -> None:
        """
        Writes assembly code that affects the goto command.
        :param label: The label to go to.
        """
        self._output_stream.write(f"// goto {label}\n")
        self._output_stream.write(f"@{label}\n")
        self._output_stream.write("0;JMP\n\n")

    def write_if(self, label: str) -> None:
        """
        Writes assembly code that affects the if-goto command.
        :param label: The label to go to.
        """
        self._output_stream.write(f"// if-goto {label}\n")
        self._output_stream.write("@SP\n")
        self._output_stream.write("AM=M-1\n")
        self._output_stream.write("D=M\n")
        self._output_stream.write(f"@{label}\n")
        self._output_stream.write("D;JNE\n\n")

    def write_function(self, function_name: str, n_vars: int) -> None:
        """
        Writes assembly code that affects the function command.
        The handling of each "function Xxx.foo" command within the file Xxx.vm
        generates and injects a symbol "Xxx.foo" into the assembly code stream
        that labels the entry-point to the function's code.
        In the subsequent assembly process, the assembler translates this
        symbol into the physical address where the function code starts.
        Operates as follows:
            (function_name)
            repeat n_vars times:
                push constant 0
        :param function_name: The name of the function.
        :param n_vars: The number of local variables of the function.
        """
        self._output_stream.write(f"// function {function_name} {n_vars}\n")
        self.write_label(function_name)
        for i in range(n_vars):
            self.push_stack("0")

    def save_pointer(self, pointer) -> None:
        """
        Saves the pointer to the frame.
        :param pointer: The pointer to save.
        """
        self._output_stream.write(f"@{pointer}\n")
        self._output_stream.write("D=M\n")
        self.push_stack("D")

    def write_call(self, function_name: str, n_args: int) -> None:
        """
        Writes assembly code that affects the call command.
        Let "Xxx.foo" be a function within the file Xxx.vm.
        The handling of each "call" command within Xxx.foo's code generates and
        injects a symbol "Xxx.foo$ret.i" into the assembly code stream, where
        "i" is a running integer (one such symbol is generated for each "call"
        command within "Xxx.foo").
        This symbol is used to mark the return address within the caller's
        code. In the subsequent assembly process, the assembler translates this
        symbol into the physical memory address of the command immediately
        following the "call" command.
        Operates as follows:
            push return_address
            push LCL
            push ARG
            push THIS
            push THAT
            ARG = SP - 5 - n_args
            LCL = SP
            goto function_name
            (return_address)
        :param function_name: The name of the function to call.
        :param n_args: The number of arguments of the function.
        """
        self._output_stream.write(f"// call {function_name} {n_args}\n")
        self._function_call_counter += 1
        self._output_stream.write(f"@{self._file_name}$ret.{self._function_call_counter}\n")
        self._output_stream.write("D=A\n")
        self.push_stack("D")
        self.save_pointer("LCL")
        self.save_pointer("ARG")
        self.save_pointer("THIS")
        self.save_pointer("THAT")
        self._output_stream.write("@SP\n")
        self._output_stream.write("D=M\n")
        self._output_stream.write(f"@{n_args + 5}\n")
        self._output_stream.write("D=D-A\n")
        self._output_stream.write("@ARG\n")
        self._output_stream.write("M=D\n")
        self._output_stream.write("@SP\n")
        self._output_stream.write("D=M\n")
        self._output_stream.write("@LCL\n")
        self._output_stream.write("M=D\n")
        self.write_goto(function_name)
        self.write_label(f"{self._file_name}$ret.{self._function_call_counter}")

    def restore_pointer(self, pointer) -> None:
        """
        Restores the pointer to the value stored in the frame.
        :param pointer: The pointer to restore.
        """
        self._output_stream.write("@R14\n")
        self._output_stream.write("M=M-1\n")
        self._output_stream.write("A=M\n")
        self._output_stream.write("D=M\n")
        self._output_stream.write(f"@{pointer}\n")
        self._output_stream.write("M=D\n")

    def write_return(self) -> None:
        """
        Writes assembly code that affects the return command.
        Operates as follows:
            frame = LCL
            return_address = *(frame-5)
            *ARG = pop()
            SP = ARG + 1
            THAT = *(frame-1)
            THIS = *(frame-2)
            ARG = *(frame-3)
            LCL = *(frame-4)
            goto return_address
        """
        self._output_stream.write("// return\n")
        self._output_stream.write("@LCL\n")
        self._output_stream.write("D=M\n")
        self._output_stream.write("@R14\n")
        self._output_stream.write("M=D\n")
        self._output_stream.write("@5\n")
        self._output_stream.write("D=A\n")
        self._output_stream.write("@R14\n")
        self._output_stream.write("D=M-D\n")
        self._output_stream.write("A=D\n")
        self._output_stream.write("D=M\n")
        self._output_stream.write("@R15\n")
        self._output_stream.write("M=D\n")
        self.pop_stack("argument", '0')
        self._output_stream.write("@ARG\n")
        self._output_stream.write("D=M\n")
        self._output_stream.write("@SP\n")
        self._output_stream.write("M=D+1\n")
        self.restore_pointer("THAT")
        self.restore_pointer("THIS")
        self.restore_pointer("ARG")
        self.restore_pointer("LCL")
        self._output_stream.write("@R15\n")
        self._output_stream.write("A=M\n")
        self._output_stream.write("0;JMP\n")
        self._output_stream.write("\n")

    def write_init(self) -> None:
        """
        Writes the assembly code that is the translation of the bootstrap code:
            SP = 256
            call Sys.init 0
        """
        self._output_stream.write("// bootstrap code\n")
        self._output_stream.write("@256\n")
        self._output_stream.write("D=A\n")
        self._output_stream.write("@SP\n")
        self._output_stream.write("M=D\n")
        self.write_call("Sys.init", 0)
        self._output_stream.write("\n")
