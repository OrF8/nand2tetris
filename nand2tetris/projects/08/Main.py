"""
This _output_stream is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
from typing import TextIO
from Parser import Parser
from CodeWriter import CodeWriter


def translate_file(in_file: TextIO, out_file: TextIO, is_bootstrap: bool = False) -> None:
    """
    Translates a single _output_stream from VM code to Hack assembly code.
    :param in_file: The _output_stream to translate.
    :param out_file: Where to write the translated code.
    :param bootstrap: Whether to write the bootstrap code.
    """
    parser = Parser(input_file)
    code_writer = CodeWriter(output_file, input_file.name.split('\\')[-1].split('.')[0])
    if is_bootstrap:
        code_writer.write_init()
    while parser.has_more_commands():
        parser.advance()
        command_type = parser.command_type()
        if command_type == "C_ARITHMETIC":
            code_writer.write_arithmetic(parser.arg1())
        elif command_type in ["C_PUSH", "C_POP"]:
            code_writer.write_push_pop(command_type, parser.arg1(), parser.arg2())
        elif command_type == "C_LABEL":
            code_writer.write_label(parser.arg1())
        elif command_type == "C_GOTO":
            code_writer.write_goto(parser.arg1())
        elif command_type == "C_IF":
            code_writer.write_if(parser.arg1())
        elif command_type == "C_FUNCTION":
            code_writer.write_function(parser.arg1(), parser.arg2())
        elif command_type == "C_RETURN":
            code_writer.write_return()
        elif command_type == "C_CALL":
            code_writer.write_call(parser.arg1(), parser.arg2())


if "__main__" == __name__:
    # Parses the input path and calls translate_file on each input _output_stream.
    # This opens both the input and the output files!
    # Both are closed automatically when the code finishes running.
    # If the output _output_stream does not exist, it is created automatically in the
    # correct path, using the correct filename.
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: VMtranslator <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_translate = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
        output_path = os.path.join(argument_path, os.path.basename(
            argument_path))
    else:
        files_to_translate = [argument_path]
        output_path, extension = os.path.splitext(argument_path)
    output_path += ".asm"
    bootstrap = True
    with open(output_path, 'w') as output_file:
        for input_path in files_to_translate:
            filename, extension = os.path.splitext(input_path)
            if extension.lower() != ".vm":
                continue
            with open(input_path, 'r') as input_file:
                translate_file(input_file, output_file, bootstrap)
            bootstrap = False
