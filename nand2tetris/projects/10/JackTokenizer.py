"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""

import re
from typing import TextIO, Union, Tuple, List


class JackTokenizer:
    """
    Removes all comments from the input stream and breaks it
    into Jack language _tokens, as specified by the Jack grammar.
    
    # Jack Language Grammar

    A Jack file is a stream of characters. If the file represents a
    valid program, it can be tokenized into a stream of valid _tokens. The
    _tokens may be separated by an arbitrary number of whitespace characters
    and comments, which are ignored. There are three possible comment formats: 
    /* comment until closing */, /** API comment until closing */, and
    // comment until the line's end.

    - 'xxx': quotes are used for _tokens that appear verbatim ('terminals').
    - xxx: regular typeface is used for names of language constructs ('non-terminals').
    - (): parentheses are used for grouping of language constructs.
    - x | y: indicates that either x or y can appear.
    - x?: indicates that x appears 0 or 1 times.
    - x*: indicates that x appears 0 or more times.

    ## Lexical Elements

    The Jack language includes five types of terminal elements (_tokens).

    - keyword: 'class' | 'constructor' | 'function' | 'method' | 'field' | 
               'static' | 'var' | 'int' | 'char' | 'boolean' | 'void' | 'true' |
               'false' | 'null' | 'this' | 'let' | 'do' | 'if' | 'else' | 
               'while' | 'return'
    - symbol: '{' | '}' | '(' | ')' | '[' | ']' | '.' | ',' | ';' | '+' | 
              '-' | '*' | '/' | '&' | '|' | '<' | '>' | '=' | '~' | '^' | '#'
    - integerConstant: A decimal number in the range 0-32767.
    - StringConstant: '"' A sequence of Unicode characters not including 
                      double quote or newline '"'
    - identifier: A sequence of letters, digits, and underscore ('_') not 
                  starting with a digit. You can assume keywords cannot be
                  identifiers, so 'self' cannot be an identifier, etc.

    ## Program Structure

    A Jack program is a collection of classes, each appearing in a separate 
    file. A compilation unit is a single class. A class is a sequence of _tokens
    structured according to the following context-free syntax:
    
    - class: 'class' className '{' classVarDec* subroutineDec* '}'
    - classVarDec: ('static' | 'field') type varName (',' varName)* ';'
    - type: 'int' | 'char' | 'boolean' | className
    - subroutineDec: ('constructor' | 'function' | 'method') ('void' | type) 
    - subroutineName '(' parameterList ')' subroutineBody
    - parameterList: ((type varName) (',' type varName)*)?
    - subroutineBody: '{' varDec* statements '}'
    - varDec: 'var' type varName (',' varName)* ';'
    - className: identifier
    - subroutineName: identifier
    - varName: identifier

    ## Statements

    - statements: statement*
    - statement: letStatement | ifStatement | whileStatement | doStatement | 
                 returnStatement
    - letStatement: 'let' varName ('[' expression ']')? '=' expression ';'
    - ifStatement: 'if' '(' expression ')' '{' statements '}' ('else' '{' 
                   statements '}')?
    - whileStatement: 'while' '(' 'expression' ')' '{' statements '}'
    - doStatement: 'do' subroutineCall ';'
    - returnStatement: 'return' expression? ';'

    ## Expressions
    
    - expression: term (op term)*
    - term: integerConstant | stringConstant | KEYWORD_CONST | varName |
            varName '['expression']' | subroutineCall | '(' expression ')' | 
            UNARY_OPERATION term
    - subroutineCall: subroutineName '(' expressionList ')' | (className | 
                      varName) '.' subroutineName '(' expressionList ')'
    - expressionList: (expression (',' expression)* )?
    - op: '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='
    - UNARY_OPERATION: '-' | '~' | '^' | '#'
    - KEYWORD_CONST: 'true' | 'false' | 'null' | 'this'
    
    Note that ^, # correspond to shiftleft and shiftright, respectively.
    """

    def __init__(self, input_stream: TextIO) -> None:
        """
        Opens the input stream and gets ready to tokenize it.

        :param input_stream: The input stream.
        """
        # Your code goes here!
        # A good place to start is to read all the lines of the input:
        # input_lines = input_stream.read().splitlines()
        self._current_token: Tuple[str, Union[str, int]] = ('', '')
        self._tokens: List[Tuple[str, Union[str, int]]] = []
        self._current_token_index: int = -1
        self._tokenize(input_stream.read())

    def _tokenize(self, input_data: str) -> None:
        """
        Tokenizes the input data and stores the _tokens in self._tokens.
        :param input_data: The input data to tokenize.
        """
        token_specification = [
            ('COMMENT', r'//.*|/\*[\s\S]*?\*/|/\*\*[\s\S]*?\*/'),
            ('keyword', r'\b(class|constructor|function|method|field|static|var|int|char|boolean|void|true|false|null'
                        r'|this|let|do|if|else|while|return)\b'),
            ('symbol', r'[{}()\[\].,;+\-*/&|<>=~^#]'),
            ('integerConstant', r'\b\d+\b'),
            ('stringConstant', r'"[^"\n]*"'),
            ('identifier', r'\b[a-zA-Z_]\w*\b'),
            ('SKIP', r'[ \t\n]+')
        ]
        tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)
        for mo in re.finditer(tok_regex, input_data):
            kind = mo.lastgroup
            value = mo.group()
            if kind == 'SKIP' or kind == 'COMMENT':
                continue
            elif kind == 'stringConstant':
                value = value[1:-1]
            elif kind == 'integerConstant':
                value = int(value)
            self._tokens.append((kind, value))

    def has_more_tokens(self) -> bool:
        """
        Do we have more _tokens in the input?

        :return: True if there are more _tokens, False otherwise.
        """
        return self._current_token_index < len(self._tokens) - 1

    def advance(self) -> Tuple[str, Union[str, int]]:
        """
        Gets the next token from the input and makes it the current token.
        This method should be called if has_more_tokens() is true. 
        Initially, there is no current token.
        """
        if self.has_more_tokens():
            self._current_token_index += 1
            self._current_token = self._tokens[self._current_token_index]
            return self._current_token

    def value(self) -> Union[str, int]:
        """
        :return: The current value of the current token.
        """
        return self._current_token[1]

    def peek(self) -> Tuple[str, Union[str, int]]:
        """
        :return: The next token in the input, without advancing.
        """
        if self._current_token_index < len(self._tokens) - 1:
            return self._tokens[self._current_token_index + 1]
        return '', ''

    def token(self) -> str:
        """
        :return: The type of the current token, can be:
                 "KEYWORD", "SYMBOL", "IDENTIFIER", "INT_CONST", "STRING_CONST"
        """
        return self._current_token[0]

    def keyword(self) -> str:
        """
        :return: The keyword which is the current token.
                 Should be called only when token_type() is "KEYWORD".
                 Can return "CLASS", "METHOD", "FUNCTION", "CONSTRUCTOR", "INT",
                 "BOOLEAN", "CHAR", "VOID", "VAR", "STATIC", "FIELD", "LET", "DO",
                 "IF", "ELSE", "WHILE", "RETURN", "TRUE", "FALSE", "NULL", "THIS"
        """
        return self._current_token[1]

    def symbol(self) -> str:
        """
        :return: str: the character which is the current token.
                 Should be called only when token_type() is "SYMBOL".
                 Recall that symbol was defined in the grammar like so:
                 symbol: '{' | '}' | '(' | ')' | '[' | ']' | '.' | ',' | ';' | '+' |
                 '-' | '*' | '/' | '&' | '|' | '<' | '>' | '=' | '~' | '^' | '#'
        """
        return self._current_token[1]

    def identifier(self) -> str:
        """
        :return: str: the identifier which is the current token.
                 Should be called only when token_type() is "IDENTIFIER".
                 Recall that identifiers were defined in the grammar like so:
                 identifier: A sequence of letters, digits, and underscore ('_') not
                 starting with a digit. You can assume keywords cannot be
                 identifiers, so 'self' cannot be an identifier, etc.
        """
        return self._current_token[1]

    def int_val(self) -> int:
        """
        :return: str: the integer value of the current token.
                 Should be called only when token_type() is "INT_CONST".
                 Recall that integerConstant was defined in the grammar like so:
                 integerConstant: A decimal number in the range 0-32767.
        """
        return self._current_token[1]

    def string_val(self) -> str:
        """
        :return: str: the string value of the current token, without the double
                 quotes. Should be called only when token_type() is "STRING_CONST".
                 Recall that StringConstant was defined in the grammar like so:
                 StringConstant: '"' A sequence of Unicode characters not including double quote or newline '"'
        """
        return self._current_token[1]
