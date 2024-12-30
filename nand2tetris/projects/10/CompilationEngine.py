"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""

from typing import TextIO
from JackTokenizer import JackTokenizer


class CompilationEngine:
    """
    Gets input from a JackTokenizer and emits its parsed structure into an
    _output stream.
    """

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
        if token_type == "symbol":
            if token == "<":
                token = "&lt;"
            elif token == ">":
                token = "&gt;"
            elif token == "&":
                token = "&amp;"
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
        self._write_non_terminal_start("class")

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
        while self._tokenizer.value() in ["static", "field"]:
            self._compile_var_dec(True)
        while self._tokenizer.value() in ["constructor", "function", "method"]:
            self._compile_subroutine()

        # }
        self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
        self._write_non_terminal_end("class")

    def _compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        self._write_non_terminal_start("subroutineDec")

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
        self._write_non_terminal_start("subroutineBody")

        # {
        self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
        self._tokenizer.advance()

        # varDec*
        while self._tokenizer.value() == "var":
            self._compile_var_dec()

        # statements
        self._compile_statements()

        # }
        self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
        self._tokenizer.advance()

        self._write_non_terminal_end("subroutineBody")
        self._write_non_terminal_end("subroutineDec")

    def _compile_parameter_list(self) -> None:
        """
        Compiles a (possibly empty) parameter list, not including the
        enclosing "()".
        """
        self._write_non_terminal_start("parameterList")

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

        self._write_non_terminal_end("parameterList")

    def _compile_var_dec(self, is_class=False) -> None:
        """
        Compiles a var declaration.
        :param is_class: Whether the var declaration is a class var declaration.
        """
        self._write_non_terminal_start("classVarDec" if is_class else "varDec")

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

        self._write_non_terminal_end("classVarDec" if is_class else "varDec")

    def _compile_statements(self) -> None:
        """
        Compiles a sequence of statements, not including the enclosing
        "{}".
        """
        self._write_non_terminal_start("statements")

        while self._tokenizer.value() in ["let", "if", "while", "do", "return"]:
            if self._tokenizer.value() == "let":
                self._compile_let()
            elif self._tokenizer.value() == "if":
                self._compile_if()
            elif self._tokenizer.value() == "while":
                self._compile_while()
            elif self._tokenizer.value() == "do":
                self._compile_do()
            elif self._tokenizer.value() == "return":
                self._compile_return()

        self._write_non_terminal_end("statements")

    def _compile_do(self) -> None:
        """Compiles a do statement."""
        self._write_non_terminal_start("doStatement")

        # do
        self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
        self._tokenizer.advance()

        # subroutineCall
        self._compile_subroutine_call()

        # ;
        self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
        self._tokenizer.advance()

        self._write_non_terminal_end("doStatement")

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
        self._write_non_terminal_start("letStatement")

        # let
        self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
        self._tokenizer.advance()

        # varName
        self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
        self._tokenizer.advance()

        # ('[' expression ']')?
        if self._tokenizer.value() == "[":
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

        self._write_non_terminal_end("letStatement")

    def _compile_while(self) -> None:
        """Compiles a while statement."""
        self._write_non_terminal_start("whileStatement")

        self._compile_if_while_body()

        self._write_non_terminal_end("whileStatement")

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
        self._write_non_terminal_start("returnStatement")

        # return
        self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
        self._tokenizer.advance()

        # expression?
        if self._tokenizer.value() != ";":
            self._compile_expression()

        # ;
        self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
        self._tokenizer.advance()

        self._write_non_terminal_end("returnStatement")

    def _compile_if(self) -> None:
        """Compiles an if statement, possibly with a trailing else clause."""
        self._write_non_terminal_start("ifStatement")

        self._compile_if_while_body()

        # (else { statements })?
        if self._tokenizer.value() == "else":
            self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
            self._tokenizer.advance()

            self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
            self._tokenizer.advance()

            self._compile_statements()

            self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
            self._tokenizer.advance()

        self._write_non_terminal_end("ifStatement")

    def _compile_expression(self) -> None:
        """Compiles an expression."""
        self._write_non_terminal_start("expression")

        # term
        self._compile_term()

        # (op term)*
        while self._tokenizer.value() in ["+", "-", "*", "/", "&", "|", "<", ">", "="]:
            self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
            self._tokenizer.advance()
            self._compile_term()

        self._write_non_terminal_end("expression")

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
        self._write_non_terminal_start("term")

        if self._tokenizer.value() in ["true", "false", "null", "this"]:
            self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
            self._tokenizer.advance()
        elif self._tokenizer.value() in ["-", "~"]:
            self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
            self._tokenizer.advance()
            self._compile_term()
        elif self._tokenizer.value() == "(":
            self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
            self._tokenizer.advance()
            self._compile_expression()
            self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
            self._tokenizer.advance()
        else:  # identifier
            self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
            self._tokenizer.advance()

            if self._tokenizer.value() == "[":  # array
                self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
                self._tokenizer.advance()
                self._compile_expression()
                self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
                self._tokenizer.advance()
            elif self._tokenizer.value() in ["(", "."]:  # subroutine call
                if self._tokenizer.value() == ".":
                    self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
                    self._tokenizer.advance()
                    self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
                    self._tokenizer.advance()

                self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
                self._tokenizer.advance()
                self._compile_expression_list()
                self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
                self._tokenizer.advance()

        self._write_non_terminal_end("term")

    def _compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        self._write_non_terminal_start("expressionList")

        if self._tokenizer.value() != ")":
            self._compile_expression()
            while self._tokenizer.value() == ",":
                self._write_terminal(self._tokenizer.token(), self._tokenizer.value())
                self._tokenizer.advance()
                self._compile_expression()

        self._write_non_terminal_end("expressionList")
