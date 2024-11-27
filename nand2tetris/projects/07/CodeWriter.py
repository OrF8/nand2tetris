"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
from typing import TextIO
from MapVars import INVERSE_COMMAND_MAP, SEGMENT_MAP, THIS_THAT_MAP


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

    def __init__(self, output_stream: TextIO) -> None:
        """
        Initializes the CodeWriter.
        :param output_stream: Output stream.
        """
        self._output_stream: TextIO = output_stream
        self._file_name: str = output_stream.name.split('\\')[-1].split('.')[0]
        self._TMP_INDEX: int = 5
        self._jmp_index: int = 1

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
            self._output_stream.write("M=M<<1\n")
        elif command == "shiftright":
            self._output_stream.write("M=M>>1\n")

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

    def _push_constant(self, index: int) -> None:
        """
        Writes the assembly code for pushing or popping a constant.
        Operates as follows:
            *SP = index
            SP++
        :param index: The constant to push or pop.
        """
        self._output_stream.write(f"// push constant {index}\n")
        self._output_stream.write(f"@{index} // D={index}\n")
        self._output_stream.write("D=A\n")
        self._output_stream.write("@SP // *SP=D\n")
        self._output_stream.write("A=M\n")
        self._output_stream.write("M=D\n")
        self._output_stream.write("@SP // SP++\n")
        self._output_stream.write("M=M+1\n\n")

    def _push_latt(self, segment: str, index: int) -> None:
        """
        Writes the assembly code for pushing a local, argument, this, or that segment.
        Operates as follows:
            addr = segment + index
            *SP = *addr
            SP++
        :param segment: The memory segment to operate on.
        :param index: The index in the memory segment.
        """
        self._output_stream.write(f"@{index} // D=index\n")
        self._output_stream.write("D=A\n")
        self._output_stream.write(f"@{segment} // D=segment + index\n")
        self._output_stream.write("A=M+D\n")
        self._output_stream.write("D=A\n")
        self._output_stream.write("@R13 // R13=addr\n")
        self._output_stream.write("M=D\n")
        self._output_stream.write("@R13 // D=*addr\n")
        self._output_stream.write("A=M\n")
        self._output_stream.write("D=M\n")
        self._output_stream.write("@SP // *SP=D\n")
        self._output_stream.write("A=M\n")
        self._output_stream.write("M=D\n")
        self._output_stream.write("@SP // SP++\n")
        self._output_stream.write("M=M+1\n")

    def _pop_latt(self, segment: str, index: int) -> None:
        """
        Writes the assembly code for popping a local, argument, this, or that segment.
        Operates as follows:
            addr = segment + index
            SP--
            *addr = *SP
        :param segment: The memory segment to operate on.
        :param index: The index in the memory segment.
        """
        self._output_stream.write(f"@{index} // D=index\n")
        self._output_stream.write("D=A\n")
        self._output_stream.write(f"@{segment} // D=segment + index\n")
        self._output_stream.write("A=M+D\n")
        self._output_stream.write("D=A\n")
        self._output_stream.write("@R13 // R13=addr\n")
        self._output_stream.write("M=D\n")
        self._output_stream.write("@SP // SP--\n")
        self._output_stream.write("AM=M-1\n")
        self._output_stream.write("D=M\n")
        self._output_stream.write("@R13 // *addr=*SP\n")
        self._output_stream.write("A=M\n")
        self._output_stream.write("M=D\n")

    def _push_pop_latt(self, command: str, segment, index: int) -> None:
        """
        Writes the assembly code for pushing or popping a local, argument, this, or that segment.
        :param command: The command type (push or pop).
        :param segment: The memory segment to operate on.
        :param index: The index in the memory segment.
        """
        self._output_stream.write(f"// {command} {segment} {index}\n")
        segment = SEGMENT_MAP[segment]
        if command == "push":
            self._push_latt(segment, index)
        elif command == "pop":
            self._pop_latt(segment, index)
        self._output_stream.write("\n")

    def _push_temp(self, index: int) -> None:
        """
        Writes the assembly code for pushing a temp segment.
        Operates as follows:
            addr = 5 + index (_TMP_INDEX + index)
            *SP = *addr
            SP++
        :param index: The index in the temp segment.
        """
        self._output_stream.write("D=M // D=*addr\n")
        self._output_stream.write("@SP // *SP=*addr\n")
        self._output_stream.write("A=M\n")
        self._output_stream.write("M=D\n")
        self._output_stream.write("@SP // SP++\n")
        self._output_stream.write("M=M+1\n")

    def _pop_temp(self, index: int) -> None:
        """
        Writes the assembly code for popping a temp segment.
        Operates as follows:
            addr = 5 + index (_TMP_INDEX + index)
            SP--
            *addr = *SP
        :param index: The index in the temp segment.
        """
        self._output_stream.write("D=A // D=addr\n")
        self._output_stream.write("@R13 // R13=addr\n")
        self._output_stream.write("M=D\n")
        self._output_stream.write("@SP // SP--\n")
        self._output_stream.write("AM=M-1\n")
        self._output_stream.write("D=M // D=*SP\n")
        self._output_stream.write("@R13 // *addr=*SP\n")
        self._output_stream.write("A=M\n")
        self._output_stream.write("M=D\n")

    def _push_pop_temp(self, command: str, index: int) -> None:
        """
        Writes the assembly code for pushing or popping a temp segment.
        :param command: The command type (push or pop).
        :param index: The index in the temp segment.
        """
        self._output_stream.write(f"// {command} temp {index}\n")
        # To be able to accept indices that are not in the range [0, 7], I decided to use the following formula:
        #        { 5 + (index % 7) if index%7 != 0 or index == 0
        # addr = {
        #        { 12 else
        self._output_stream.write(f"@{self._TMP_INDEX + (index % 7) if index % 7 != 0 or index != 0 else 12}\n")
        if command == "push":
            self._push_temp(index)
        elif command == "pop":
            self._pop_temp(index)
        self._output_stream.write("\n")

    def _push_pointer(self, index: int) -> None:
        """
        Writes the assembly code for pushing a pointer segment.
        Operates as follows:
            *SP = THIS/THAT
            SP++
        :param index: The index in the pointer segment.
        """
        self._output_stream.write(f"@{THIS_THAT_MAP[index]} // D=THIS/THAT\n")
        self._output_stream.write("D=M\n")
        self._output_stream.write("@SP // *SP=D\n")
        self._output_stream.write("A=M\n")
        self._output_stream.write("M=D\n")
        self._output_stream.write("@SP // SP++\n")
        self._output_stream.write("M=M+1\n")

    def _pop_pointer(self, index: int) -> None:
        """
        Writes the assembly code for popping a pointer segment.
        Operates as follows:
            SP--
            THIS/THAT = *SP
        :param index: The index in the pointer segment.
        """
        self._output_stream.write("@SP // SP--\n")
        self._output_stream.write("AM=M-1\n")
        self._output_stream.write("D=M // D = RAM[SP]\n")
        self._output_stream.write(f"@{THIS_THAT_MAP[index]} // THIS/THAT=*SP\n")
        self._output_stream.write("M=D\n")

    def _push_pop_pointer(self, command: str, index: int) -> None:
        """
        Writes the assembly code for pushing or popping a pointer segment.
        To be able to accept indices that are not in {0, 1}, I decided to use this function: pointer = (index % 2).
        :param command: The command type (push or pop).
        :param index: The index in the pointer segment.
        """
        self._output_stream.write(f"// {command} pointer {index}\n")
        if command == "push":
            self._push_pointer(index)
        else:
            self._pop_pointer(index)
        self._output_stream.write("\n")

    def _pop_static(self, index: int) -> None:
        """
        Writes the assembly code for popping a static segment.
        Operates as follows:
            D = stack.pop()
            var filename.static_index = D
        :param index: The index in the static segment.
        """
        self._output_stream.write("@SP\n")
        self._output_stream.write("AM=M-1\n")
        self._output_stream.write("D=M\n")
        self._output_stream.write(f"@{self._file_name}.{index}\n")
        self._output_stream.write("M=D\n")

    def _push_static(self, index: int) -> None:
        """
        Writes the assembly code for pushing a static segment.
        Operates as follows:
            D = var filename.static_index
            stack.push(D)
        :param index: The index in the static segment.
        """
        self._output_stream.write(f"@{self._file_name}.{index}\n")
        self._output_stream.write("D=M\n")
        self._output_stream.write("@SP\n")
        self._output_stream.write("A=M\n")
        self._output_stream.write("M=D\n")
        self._output_stream.write("@SP\n")
        self._output_stream.write("M=M+1\n")

    def _push_pop_static(self, command: str, index: int) -> None:
        """
        Writes the assembly code for pushing or popping a static segment.
        :param command: The command type (push or pop).
        :param index: The index in the static segment.
        """
        self._output_stream.write(f"// {command} static {index}\n")
        self._output_stream.write(f"@{self._file_name}.{index}\n")
        if command == "push":
            self._push_static(index)
        else:
            self._pop_static(index)
        self._output_stream.write("\n")

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
        command = INVERSE_COMMAND_MAP[command]
        if segment == "constant":
            self._push_constant(index)
        elif segment in ["local", "argument", "this", "that"]:
            self._push_pop_latt(command, segment, index)
        elif segment == "temp":
            self._push_pop_temp(command, index)
        elif segment == "pointer":
            self._push_pop_pointer(command, index % 2)
        elif segment == "static":
            self._push_pop_static(command, index)

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
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        pass

    def write_goto(self, label: str) -> None:
        """
        Writes assembly code that affects the goto command.
        :param label: The label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        pass

    def write_if(self, label: str) -> None:
        """
        Writes assembly code that affects the if-goto command.
        :param label: The label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        pass

    def write_function(self, function_name: str, n_vars: int) -> None:
        """
        Writes assembly code that affects the function command.
        The handling of each "function Xxx.foo" command within the file Xxx.vm
        generates and injects a symbol "Xxx.foo" into the assembly code stream
        that labels the entry-point to the function's code.
        In the subsequent assembly process, the assembler translates this
        symbol into the physical address where the function code starts.
        :param function_name: The name of the function.
        :param n_vars: The number of local variables of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "function function_name n_vars" is:
        # (function_name)       // injects a function entry label into the code
        # repeat n_vars times:  // n_vars = number of local variables
        #   push constant 0     // initializes the local variables to 0
        pass

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
        :param function_name: The name of the function to call.
        :param n_args: The number of arguments of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "call function_name n_args" is:
        # push return_address   // generates a label and pushes it to the stack
        # push LCL              // saves LCL of the caller
        # push ARG              // saves ARG of the caller
        # push THIS             // saves THIS of the caller
        # push THAT             // saves THAT of the caller
        # ARG = SP-5-n_args     // repositions ARG
        # LCL = SP              // repositions LCL
        # goto function_name    // transfers control to the callee
        # (return_address)      // injects the return address label into the code
        pass

    def write_return(self) -> None:
        """
        Writes assembly code that affects the return command.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "return" is:
        # frame = LCL                   // frame is a temporary variable
        # return_address = *(frame-5)   // puts the return address in a temp var
        # *ARG = pop()                  // repositions the return value for the caller
        # SP = ARG + 1                  // repositions SP for the caller
        # THAT = *(frame-1)             // restores THAT for the caller
        # THIS = *(frame-2)             // restores THIS for the caller
        # ARG = *(frame-3)              // restores ARG for the caller
        # LCL = *(frame-4)              // restores LCL for the caller
        # goto return_address           // go to the return address
        pass
