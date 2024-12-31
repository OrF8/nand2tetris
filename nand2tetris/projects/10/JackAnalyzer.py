"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
from typing import TextIO
from CompilationEngine import CompilationEngine
from JackTokenizer import JackTokenizer

DESIRED_INPUT_LENGTH: int = 2
WRONG_INPUT_LENGTH_MESSAGE: str = "Invalid usage, please use: JackAnalyzer <input path>"
INPUT_EXTENSION: str = ".jack"
OUTPUT_EXTENSION: str = ".xml"
OPEN_AS_READ: str = 'r'
OPEN_AS_WRITE: str = 'w'


def analyze_file(in_file: TextIO, out_file: TextIO) -> None:
    """
    Analyzes a single file.

    :param in_file: The file to analyze.
    :param out_file: The file to write the _output to.
    """
    tokenizer: JackTokenizer = JackTokenizer(in_file)
    engine: CompilationEngine = CompilationEngine(tokenizer, out_file)
    engine.compile_class()


if __name__ == "__main__":
    # Parses the input path and calls analyze_file on each input file.
    # This opens both the input and the _output files!
    # Both are closed automatically when the code finishes running.
    # If the _output file does not exist, it is created automatically in the
    # correct path, using the correct filename.
    if not len(sys.argv) == DESIRED_INPUT_LENGTH:
        sys.exit(WRONG_INPUT_LENGTH_MESSAGE)
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_assemble = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
    else:
        files_to_assemble = [argument_path]
    for input_path in files_to_assemble:
        filename, extension = os.path.splitext(input_path)
        if extension.lower() != INPUT_EXTENSION:
            continue
        output_path = filename + OUTPUT_EXTENSION
        with open(input_path, OPEN_AS_READ) as input_file, \
                open(output_path, OPEN_AS_WRITE) as output_file:
            analyze_file(input_file, output_file)
