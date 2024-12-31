"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""

from typing import TextIO, Dict, List
from JackTokenizer import JackTokenizer


class CompilationEngine:
    """
    Gets input from a JackTokenizer and emits its parsed structure into an
    _output stream.
    """

    _SYMBOL_TOKEN: str = "symbol"
    _SPECIAL_SYMBOL_MAP: Dict[str, str] = {
        "<": "&lt;",
        ">": "&gt;",
        "&": "&amp;"
    }
    _CLASS_HEADER = "class"
    _VAR_DECS: List[str] = ["static", "field"]
    _SUBROUTINE_DECS: List[str] = ["constructor", "function", "method"]
    _SUBROUTINE_DEC_HEADER: str = "subroutineDec"
    _SUBROUTINE_BODY_HEADER: str = "subroutineBody"
    _VAR_TOKEN: str = "var"
    _PARAMETER_LIST_HEADER: str = "parameterList"
    _CLASS_VAR_DEC_HEADER: str = "classVarDec"
    _VAR_DEC_HEADER: str = "varDec"
    _STATEMENTS_HEADER: str = "statements"
    _LET_TOKEN: str = "let"
    _IF_TOKEN: str = "if"
    _WHILE_TOKEN: str = "while"
    _DO_TOKEN: str = "do"
    _RETURN_TOKEN: str = "return"
    _STATEMENTS_LIST: List[str] = [_LET_TOKEN, _IF_TOKEN, _WHILE_TOKEN, _DO_TOKEN, _RETURN_TOKEN]
    _DO_STATEMENT_HEADER: str = "doStatement"
    _LET_STATEMENT_HEADER: str = "letStatement"
    _START_OF_EXPRESSION_INDEXING: str = "["
    _WHILE_STATEMENT_HEADER: str = "whileStatement"
    _RETURN_STATEMENT_HEADER: str = "returnStatement"
    _IF_STATEMENT_HEADER: str = "ifStatement"
    _ELSE_STATEMENT: str = "else"
    _EXPRESSION_HEADER: str = "expression"
    _SYMBOLS_LIST: List[str] = ["+", "-", "*", "/", "&", "|", "<", ">", "="]
    _TERM_HEADER: str = "term"
    _CONSTANT_LIST: List[str] = ["true", "false", "null", "this"]
    _PRE_TERM_CONSTANT_LIST: List[str] = ["-", "~"]
    _LEFT_PARENTHESIS: str = "("
    _DOT: str = "."
    _START_OF_SUBROUTINE_CALL: List[str] = ["(", _DOT]
    _EXPRESSION_LIST_HEADER: str = "expressionList"
    _RIGHT_PARENTHESIS: str = ")"
    _COMMA: str = ","

    def __init__(self, input_stream: JackTokenizer, output_stream: TextIO) -> None:
        """
        Creates a new compilation engine with the given input and _output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The _output stream.
        """
        self._tokenizer: JackTokenizer = input_stream
        self._output: TextIO = output_stream
        self._indent_level: int = 0

    def _write_terminal(self, token_type: str, token: str) -> None:
        indent: str = "  " * self._indent_level
        if token_type == self._SYMBOL_TOKEN:
            token = self._SPECIAL_SYMBOL_MAP.get(token, token)
        self._output.write(f"{indent}<{token_type}> {token} </{token_type}>\n")

    def _write_non_terminal_start(self, name: str) -> None:
        indent: str = "  " * self._indent_level
        self._output.write(f"{indent}<{name}>\n")
        self._indent_level += 1

    def _write_non_terminal_end(self, name: str) -> None:
        self._indent_level -= 1
        indent: str = "  " * self._indent_level
        self._output.write(f"{indent}</{name}>\n")

    def compile_class(self) -> None:
        """Compiles a complete class."""
        self._tokenizer.advance()
        self._write_non_terminal_start(self._CLASS_HEADER)

        # class
        self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
        self._tokenizer.advance()

        # className
        self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
        self._tokenizer.advance()

        # {
        self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
        self._tokenizer.advance()

        # classVarDec* subroutineDec*
        while self._tokenizer.value() in self._VAR_DECS:
            self._compile_var_dec(True)
        while self._tokenizer.value() in self._SUBROUTINE_DECS:
            self._compile_subroutine()

        # }
        self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
        self._write_non_terminal_end(self._CLASS_HEADER)

    def _compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        self._write_non_terminal_start(self._SUBROUTINE_DEC_HEADER)

        # constructor/function/method
        self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
        self._tokenizer.advance()

        # void/type
        self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
        self._tokenizer.advance()

        # subroutineName
        self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
        self._tokenizer.advance()

        # (
        self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
        self._tokenizer.advance()

        # parameterList
        self._compile_parameter_list()

        # )
        self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
        self._tokenizer.advance()

        # subroutineBody
        self._write_non_terminal_start(self._SUBROUTINE_BODY_HEADER)

        # {
        self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
        self._tokenizer.advance()

        # varDec*
        while self._tokenizer.value() == self._VAR_TOKEN:
            self._compile_var_dec()

        # statements
        self._compile_statements()

        # }
        self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
        self._tokenizer.advance()

        self._write_non_terminal_end(self._SUBROUTINE_BODY_HEADER)
        self._write_non_terminal_end(self._SUBROUTINE_DEC_HEADER)

    def _compile_parameter_list(self) -> None:
        """
        Compiles a (possibly empty) parameter list, not including the
        enclosing "()".
        """
        self._write_non_terminal_start(self._PARAMETER_LIST_HEADER)

        if self._tokenizer.value() != ")":
            # type
            self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
            self._tokenizer.advance()

            # varName
            self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
            self._tokenizer.advance()

            # (',' type varName)*
            while self._tokenizer.value() == ",":
                self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
                self._tokenizer.advance()

                self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
                self._tokenizer.advance()

                self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
                self._tokenizer.advance()

        self._write_non_terminal_end(self._PARAMETER_LIST_HEADER)

    def _compile_var_dec(self, is_class=False) -> None:
        """
        Compiles a var declaration.
        :param is_class: Whether the var declaration is a class var declaration.
        """
        self._write_non_terminal_start(self._CLASS_VAR_DEC_HEADER if is_class else self._VAR_DEC_HEADER)

        # var
        self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
        self._tokenizer.advance()

        # type
        self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
        self._tokenizer.advance()

        # varName
        self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
        self._tokenizer.advance()

        # (',' varName)*
        while self._tokenizer.value() == ",":
            self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
            self._tokenizer.advance()
            self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
            self._tokenizer.advance()

        # ;
        self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
        self._tokenizer.advance()

        self._write_non_terminal_end(self._CLASS_VAR_DEC_HEADER if is_class else self._VAR_DEC_HEADER)

    def _compile_statements(self) -> None:
        """
        Compiles a sequence of statements, not including the enclosing
        "{}".
        """
        self._write_non_terminal_start(self._STATEMENTS_HEADER)

        while self._tokenizer.value() in self._STATEMENTS_LIST:
            if self._tokenizer.value() == self._LET_TOKEN:
                self._compile_let()
            elif self._tokenizer.value() == self._IF_TOKEN:
                self._compile_if()
            elif self._tokenizer.value() == self._WHILE_TOKEN:
                self._compile_while()
            elif self._tokenizer.value() == self._DO_TOKEN:
                self._compile_do()
            elif self._tokenizer.value() == self._RETURN_TOKEN:
                self._compile_return()

        self._write_non_terminal_end(self._STATEMENTS_HEADER)

    def _compile_do(self) -> None:
        """Compiles a do statement."""
        self._write_non_terminal_start(self._DO_STATEMENT_HEADER)

        # do
        self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
        self._tokenizer.advance()

        # subroutineCall
        self._compile_subroutine_call()

        # ;
        self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
        self._tokenizer.advance()

        self._write_non_terminal_end(self._DO_STATEMENT_HEADER)

    def _compile_subroutine_call(self) -> None:
        """Compiles a subroutine call (subroutineName | (className | varName).subroutineName)."""
        self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
        self._tokenizer.advance()

        if self._tokenizer.value() == ".":
            self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
            self._tokenizer.advance()
            self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
            self._tokenizer.advance()

        # (
        self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
        self._tokenizer.advance()

        # expressionList
        self._compile_expression_list()

        # )
        self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
        self._tokenizer.advance()

    def _compile_let(self) -> None:
        """Compiles a let statement."""
        self._write_non_terminal_start(self._LET_STATEMENT_HEADER)

        # let
        self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
        self._tokenizer.advance()

        # varName
        self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
        self._tokenizer.advance()

        # ('[' expression ']')?
        if self._tokenizer.value() == self._START_OF_EXPRESSION_INDEXING:
            self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
            self._tokenizer.advance()
            self._compile_expression()
            self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
            self._tokenizer.advance()

        # =
        self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
        self._tokenizer.advance()

        # expression
        self._compile_expression()

        # ;
        self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
        self._tokenizer.advance()

        self._write_non_terminal_end(self._LET_STATEMENT_HEADER)

    def _compile_while(self) -> None:
        """Compiles a while statement."""
        self._write_non_terminal_start(self._WHILE_STATEMENT_HEADER)

        self._compile_if_while_body()

        self._write_non_terminal_end(self._WHILE_STATEMENT_HEADER)

    def _compile_if_while_body(self) -> None:
        """Compiles the body of an if or while statement."""
        # while or if
        self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
        self._tokenizer.advance()

        # (
        self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
        self._tokenizer.advance()

        # expression
        self._compile_expression()

        # )
        self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
        self._tokenizer.advance()

        # {
        self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
        self._tokenizer.advance()

        # statements
        self._compile_statements()

        # }
        self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
        self._tokenizer.advance()

    def _compile_return(self) -> None:
        """Compiles a return statement."""
        self._write_non_terminal_start(self._RETURN_STATEMENT_HEADER)

        # return
        self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
        self._tokenizer.advance()

        # expression?
        if self._tokenizer.value() != ";":
            self._compile_expression()

        # ;
        self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
        self._tokenizer.advance()

        self._write_non_terminal_end(self._RETURN_STATEMENT_HEADER)

    def _compile_if(self) -> None:
        """Compiles an if statement, possibly with a trailing else clause."""
        self._write_non_terminal_start(self._IF_STATEMENT_HEADER)

        self._compile_if_while_body()

        # (else { statements })?
        if self._tokenizer.value() == self._ELSE_STATEMENT:
            self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
            self._tokenizer.advance()

            self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
            self._tokenizer.advance()

            self._compile_statements()

            self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
            self._tokenizer.advance()

        self._write_non_terminal_end(self._IF_STATEMENT_HEADER)

    def _compile_expression(self) -> None:
        """Compiles an expression."""
        self._write_non_terminal_start(self._EXPRESSION_HEADER)

        # term
        self._compile_term()

        # (op term)*
        while self._tokenizer.value() in self._SYMBOLS_LIST:
            self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
            self._tokenizer.advance()
            self._compile_term()

        self._write_non_terminal_end(self._EXPRESSION_HEADER)

    def _compile_term(self) -> None:
        """
        Compiles a term.
        This routine is faced with a slight difficulty when
        trying to decide between some of the alternative parsing rules.
        Specifically, if the current token is an identifier, the routing must
        distinguish between a variable, an array entry, and a subroutine call.
        A single look-ahead token, which may be one of "[", "(", or "." suffices
        to distinguish between the three possibilities. Any other token is not
        part of this term and should not be advanced over.
        """
        self._write_non_terminal_start(self._TERM_HEADER)

        if self._tokenizer.value() in self._CONSTANT_LIST:
            self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
            self._tokenizer.advance()
        elif self._tokenizer.value() in self._PRE_TERM_CONSTANT_LIST:
            self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
            self._tokenizer.advance()
            self._compile_term()
        elif self._tokenizer.value() == self._LEFT_PARENTHESIS:
            self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
            self._tokenizer.advance()
            self._compile_expression()
            self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
            self._tokenizer.advance()
        else:  # identifier
            self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
            self._tokenizer.advance()

            if self._tokenizer.value() == self._START_OF_EXPRESSION_INDEXING:  # array
                self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
                self._tokenizer.advance()
                self._compile_expression()
                self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
                self._tokenizer.advance()
            elif self._tokenizer.value() in self._START_OF_SUBROUTINE_CALL:  # subroutine call
                if self._tokenizer.value() == self._DOT:
                    self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
                    self._tokenizer.advance()
                    self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
                    self._tokenizer.advance()

                self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
                self._tokenizer.advance()
                self._compile_expression_list()
                self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
                self._tokenizer.advance()

        self._write_non_terminal_end(self._TERM_HEADER)

    def _compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        self._write_non_terminal_start(self._EXPRESSION_LIST_HEADER)

        if self._tokenizer.value() != self._RIGHT_PARENTHESIS:
            self._compile_expression()
            while self._tokenizer.value() == self._COMMA:
                self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
                self._tokenizer.advance()
                self._compile_expression()

        self._write_non_terminal_end(self._EXPRESSION_LIST_HEADER)
