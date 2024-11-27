from typing import Dict

# Initializes a command map to translate VM commands to Hack assembly commands.
COMMAND_MAP: Dict[str, str] = {
    "push": "C_PUSH",
    "pop": "C_POP",
    "label": "C_LABEL",
    "goto": "C_GOTO",
    "if-goto": "C_IF",
    "function": "C_FUNCTION",
    "return": "C_RETURN",
    "call": "C_CALL",
    "add": "C_ARITHMETIC",
    "sub": "C_ARITHMETIC",
    "and": "C_ARITHMETIC",
    "or": "C_ARITHMETIC",
    "eq": "C_ARITHMETIC",
    "gt": "C_ARITHMETIC",
    "lt": "C_ARITHMETIC",
    "neg": "C_ARITHMETIC",
    "not": "C_ARITHMETIC",
    "shiftleft": "C_ARITHMETIC",
    "shiftright": "C_ARITHMETIC"
}

# Initializes an inverse command map to translate Hack assembly commands to VM commands.
INVERSE_COMMAND_MAP: Dict[str, str] = {
    "C_PUSH": "push",
    "C_POP": "pop",
    "C_LABEL": "label",
    "C_GOTO": "goto",
    "C_IF": "if-goto",
    "C_FUNCTION": "function",
    "C_RETURN": "return",
    "C_CALL": "call"
}

# Initializes a segment map to translate VM segment names to Hack assembly segment names.
SEGMENT_MAP: Dict[str, str] = {
    "local": "LCL",
    "argument": "ARG",
    "this": "THIS",
    "that": "THAT"
}

# Initialize a map to translate the index of the segment to the corresponding Hack assembly pointer.
THIS_THAT_MAP: Dict[int, str] = {
    0: "THIS",
    1: "THAT"
}
