"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""

from typing import TextIO, List
from JackTokenizer import JackTokenizer
from VMWriter import VMWriter
from SymbolTable import SymbolTable


class CompilationEngine:
    """
    Gets input from a JackTokenizer and emits its parsed structure into an
    _output stream.
    """

    _FIELD_DEC: str = "field"
    _VAR_DECS: List[str] = ["static", _FIELD_DEC]
    _METHOD_DEC: str = "method"
    _FUNCTION_DEC: str = "function"
    _CONSTRUCTOR_DEC: str = "constructor"
    _SUBROUTINE_DECS: List[str] = [_CONSTRUCTOR_DEC, _FUNCTION_DEC, _METHOD_DEC]
    _VAR_TOKEN: str = "var"
    _LET_TOKEN: str = "let"
    _IF_TOKEN: str = "if"
    _WHILE_TOKEN: str = "while"
    _DO_TOKEN: str = "do"
    _RETURN_TOKEN: str = "return"
    _STATEMENTS_LIST: List[str] = [_LET_TOKEN, _IF_TOKEN, _WHILE_TOKEN, _DO_TOKEN, _RETURN_TOKEN]
    _START_OF_EXPRESSION_INDEXING: str = "["
    _ELSE_STATEMENT: str = "else"
    _SYMBOLS_LIST: List[str] = ["+", "-", "*", "/", "&", "|", "<", ">", "=", "^", "#"]
    _CONSTANT_LIST: List[str] = ["true", "false", "null", "this"]
    _NEGATION: str = "~"
    _UNARY_MINUS: str = "-"
    _PRE_TERM_CONSTANT_LIST: List[str] = [_UNARY_MINUS, _NEGATION]
    _LEFT_PARENTHESIS: str = "("
    _DOT: str = "."
    _START_OF_SUBROUTINE_CALL: List[str] = [_LEFT_PARENTHESIS, _DOT]
    _RIGHT_PARENTHESIS: str = ")"
    _COMMA: str = ","
    _ENDER: str = ";"
    _CONST_SEGMENT: str = "constant"
    _POINTER_SEGMENT: str = "pointer"
    _ARGUMENT_SEGMENT: str = "argument"
    _THAT_SEGMENT: str = "that"
    _TEMP_SEGMENT: str = "temp"
    _MEMORY_ALLOCATOR: str = "Memory.alloc"
    _ADD_COMMAND: str = "add"
    _NOT_COMMAND: str = "not"
    _INTEGER_CONSTANT: str = "integerConstant"
    _STRING_CONSTANT: str = "stringConstant"
    _STRING_CREATOR: str = "String.new"
    _STRING_APPENDER: str = "String.appendChar"
    _TRUE_STRING = "true"
    _WHILE_LABEL_START: str = "WHILE_EXP"
    _WHILE_LABEL_END: str = "WHILE_END"
    _IF_LABEL_START: str = "IF_TRUE"
    _IF_LABEL_END: str = "IF_FALSE"
    _THIS_STRING: str = "this"

    def __init__(self, input_stream: JackTokenizer, output_stream: TextIO) -> None:
        """
        Creates a new compilation engine with the given input and _output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The _output stream.
        """
        self._tokenizer: JackTokenizer = input_stream
        self._vm_writer: VMWriter = VMWriter(output_stream)
        self._symbol_table: SymbolTable = SymbolTable()
        self._class_name: str = ""
        self._while_label_counter: int = 0
        self._if_label_counter: int = 0
        self._is_constructor: bool = False

    def compile_class(self) -> None:
        """Compiles a complete class."""
        self._tokenizer.advance()
        self._tokenizer.advance()  # Skip the first token ("class")

        self._class_name = self._tokenizer.value()

        self._tokenizer.advance()
        self._tokenizer.advance()  # Skip '{'

        # classVarDec* subroutineDec*
        while self._tokenizer.value() in self._VAR_DECS:
            self._compile_class_var_dec()
        while self._tokenizer.value() in self._SUBROUTINE_DECS:
            self._compile_subroutine()

    def _compile_class_var_dec(self) -> None:
        """
        Compiles a class variable declaration.
        """
        kind = self._tokenizer.value()
        self._tokenizer.advance()  # Skip the kind
        var_type = self._tokenizer.value()
        self._tokenizer.advance()  # Skip the type
        while True:
            name = self._tokenizer.value()
            self._symbol_table.define(name, var_type, kind)
            self._tokenizer.advance()  # Skip the name
            if self._tokenizer.value() == self._ENDER:
                break
            self._tokenizer.advance()  # Skip ','
        self._tokenizer.advance()  # Skip ';'

    def _compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        subroutine_type = self._tokenizer.value()
        is_method: bool = subroutine_type == self._METHOD_DEC
        self._symbol_table.start_subroutine(is_method)
        self._is_constructor = subroutine_type == self._CONSTRUCTOR_DEC
        self._tokenizer.advance()  # Skip the subroutine type
        self._tokenizer.advance()  # Skip the return type
        subroutine_name = self._tokenizer.value()
        self._tokenizer.advance()  # Skip the subroutine name
        self._tokenizer.advance()  # Skip '('
        n_locals = self._compile_parameter_list()
        self._tokenizer.advance()  # Skip ')'
        self._tokenizer.advance()  # Skip '{'
        while self._tokenizer.value() == self._VAR_TOKEN:
            n_locals += self._compile_var_dec()
        if self._is_constructor:
            self._vm_writer.write_function(f"{self._class_name}{self._DOT}{subroutine_name}", 0)
            self._vm_writer.write_push(self._CONST_SEGMENT, self._symbol_table.var_count(self._FIELD_DEC))
            self._vm_writer.write_call(self._MEMORY_ALLOCATOR, 1)
            self._vm_writer.write_pop(self._POINTER_SEGMENT, 0)
        elif is_method:
            self._vm_writer.write_function(
                f"{self._class_name}{self._DOT}{subroutine_name}", self._symbol_table.var_count(self._VAR_TOKEN)
            )
            self._vm_writer.write_push(self._ARGUMENT_SEGMENT, 0)
            self._vm_writer.write_pop(self._POINTER_SEGMENT, 0)
        else:
            self._vm_writer.write_function(f"{self._class_name}{self._DOT}{subroutine_name}", n_locals)
        self._compile_statements()
        self._tokenizer.advance()  # Skip '}'

    def _compile_parameter_list(self) -> int:
        """
        Compiles a (possibly empty) parameter list, not including the enclosing "()".

        :return: The number of local variables.
        """
        n_locals: int = 0
        if self._tokenizer.value() != self._RIGHT_PARENTHESIS:
            n_locals += 1
            var_type = self._tokenizer.value()
            self._tokenizer.advance()  # Skip the type
            name = self._tokenizer.value()
            self._symbol_table.define(name, var_type, self._ARGUMENT_SEGMENT)
            self._tokenizer.advance()  # Skip the name
            while self._tokenizer.value() == self._COMMA:
                n_locals += 1
                self._tokenizer.advance()  # Skip ','
                var_type = self._tokenizer.value()
                self._tokenizer.advance()
                name = self._tokenizer.value()
                self._symbol_table.define(name, var_type, self._ARGUMENT_SEGMENT)
                self._tokenizer.advance()
        return n_locals

    def _compile_var_dec(self) -> int:
        """
        Compiles a var declaration.

        :return: The number of variables compiled.
        """
        self._tokenizer.advance()
        num_of_vars_compiled: int = 0
        var_type = self._tokenizer.value()
        self._tokenizer.advance()
        while True:
            num_of_vars_compiled += 1
            name = self._tokenizer.value()
            self._symbol_table.define(name, var_type, self._VAR_TOKEN)
            self._tokenizer.advance()
            if self._tokenizer.value() == self._ENDER:
                break
            self._tokenizer.advance()
        self._tokenizer.advance()  # Skip ';'
        return num_of_vars_compiled

    def _compile_statements(self) -> None:
        """
        Compiles a sequence of statements, not including the enclosing "{}".
        """
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

    def _compile_do(self) -> None:
        """Compiles a do statement."""
        self._tokenizer.advance()  # Skip 'do'
        self._compile_subroutine_call()
        self._vm_writer.write_pop(self._TEMP_SEGMENT, 0)
        self._tokenizer.advance()  # Skip ';'

    def _compile_subroutine_call(self, class_name: str = None, starting_value: int = 0) -> None:
        """
        Compiles a subroutine call (subroutineName | (className | varName).subroutineName).

        :param class_name: The class name the subroutine belongs to.
        :param starting_value: The starting value of the number of arguments.
        """
        orig_name = self._tokenizer.value()
        start_value: int = starting_value
        self._tokenizer.advance()
        if self._tokenizer.value() == self._DOT:
            self._tokenizer.advance()
            if self._symbol_table.kind_of(orig_name):  # i.e., is not none.  # If it is a method called on an object
                class_name: str = self._symbol_table.type_of(orig_name)
                self._vm_writer.write_push(
                    self._symbol_table.kind_of(orig_name), self._symbol_table.index_of(orig_name)
                )
                start_value += 1
            name = f"{class_name or orig_name}{self._DOT}{self._tokenizer.value()}"
            self._tokenizer.advance()  # Skip the subroutine name
        else:
            if class_name is None:
                # It is a method called on this object
                name = f"{self._class_name}{self._DOT}{orig_name}"
                self._vm_writer.write_push(self._POINTER_SEGMENT, 0)
                start_value += 1
            else:
                # It is a function call
                name = f"{class_name}{self._DOT}{orig_name}"
        self._tokenizer.advance()  # Skip '('
        n_args = self._compile_expression_list(start_value)
        self._vm_writer.write_call(name, n_args)
        self._tokenizer.advance()  # Skip ')'

    def _compile_let(self) -> None:
        """Compiles a let statement."""
        self._tokenizer.advance()  # Skip 'let'
        name = self._tokenizer.value()
        self._tokenizer.advance()  # Skip the name
        if self._tokenizer.value() == self._START_OF_EXPRESSION_INDEXING:  # Array indexing
            # ---Handle the array indexing---
            self._tokenizer.advance()  # Skip '['
            self._compile_expression()  # Compute the index (i)
            self._tokenizer.advance()  # Skip ']'
            # Push the base address of the array
            self._vm_writer.write_push(self._symbol_table.kind_of(name), self._symbol_table.index_of(name))
            self._vm_writer.write_arithmetic(self._ADD_COMMAND)  # Add the index to the base address
            # ---Handle the value to assign---
            self._tokenizer.advance()  # Skip '='
            self._compile_expression()  # Compile the value to assign
            self._vm_writer.write_pop(self._TEMP_SEGMENT, 0)  # Assign the value to temp 0
            self._vm_writer.write_pop(self._POINTER_SEGMENT, 1)  # Save the computed address in `that` (pointer 1)
            self._vm_writer.write_push(self._TEMP_SEGMENT, 0)  # Push the value to temp 0
            self._vm_writer.write_pop(self._THAT_SEGMENT, 0)  # Assign the value to `that 0` (array)
        else:
            self._tokenizer.advance()  # Skip '='
            self._compile_expression()
            self._vm_writer.write_pop(self._symbol_table.kind_of(name), self._symbol_table.index_of(name))
        self._tokenizer.advance()  # Skip ';'

    def _compile_while(self) -> None:
        """Compiles a while statement."""
        label_true: str = f"{self._WHILE_LABEL_START}{self._while_label_counter}"
        label_false: str = f"{self._WHILE_LABEL_END}{self._while_label_counter}"
        self._while_label_counter += 1
        self._vm_writer.write_label(label_true)
        self._tokenizer.advance()
        self._tokenizer.advance()  # Skip '('
        self._compile_expression()
        self._vm_writer.write_arithmetic(self._NOT_COMMAND)
        self._vm_writer.write_if(label_false)
        self._tokenizer.advance()
        self._tokenizer.advance()  # Skip '{'
        self._compile_statements()
        self._vm_writer.write_goto(label_true)
        self._vm_writer.write_label(label_false)
        self._tokenizer.advance()

    def _compile_return(self) -> None:
        """Compiles a return statement."""
        self._tokenizer.advance()  # Skip 'return'
        if self._is_constructor:
            self._vm_writer.write_push(self._POINTER_SEGMENT, 0)
            self._tokenizer.advance()  # Skip 'this'
        elif self._tokenizer.value() != self._ENDER:
            self._compile_expression()
        else:
            self._vm_writer.write_push(self._CONST_SEGMENT, 0)
        self._vm_writer.write_return()
        self._tokenizer.advance()  # Skip ';'

    def _compile_if(self) -> None:
        """Compiles an if statement, possibly with a trailing else clause."""
        label_true: str = f"{self._IF_LABEL_START}{self._if_label_counter}"
        label_false: str = f"{self._IF_LABEL_END}{self._if_label_counter}"
        self._if_label_counter += 1
        self._tokenizer.advance()
        self._tokenizer.advance()  # Skip '('
        self._compile_expression()  # Compile the condition
        self._vm_writer.write_if(label_true)
        self._vm_writer.write_goto(label_false)
        self._vm_writer.write_label(label_true)
        self._tokenizer.advance()  # Skip ')'
        self._tokenizer.advance()  # Skip '{'
        self._compile_statements()
        self._tokenizer.advance()  # Skip '}'
        if self._tokenizer.value() == self._ELSE_STATEMENT:
            label_else_end: str = f"{label_false}_ELSE"
            self._vm_writer.write_goto(label_else_end)
            self._vm_writer.write_label(label_false)
            self._tokenizer.advance()  # Skip 'else'
            self._tokenizer.advance()  # Skip '{'
            self._compile_statements()
            self._tokenizer.advance()  # Skip '}'
            self._vm_writer.write_label(label_else_end)
        else:
            self._vm_writer.write_label(label_false)

    def _compile_expression(self) -> None:
        """Compiles an expression."""
        self._compile_term()
        while self._tokenizer.value() in self._SYMBOLS_LIST:
            op: str = self._tokenizer.value()
            self._tokenizer.advance()
            self._compile_term()
            self._vm_writer.write_arithmetic(op)

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
        if self._tokenizer.token() == self._INTEGER_CONSTANT:
            self._vm_writer.write_push(self._CONST_SEGMENT, self._tokenizer.value())
            self._tokenizer.advance()
        elif self._tokenizer.token() == self._STRING_CONSTANT:
            string = self._tokenizer.value()
            self._vm_writer.write_push(self._CONST_SEGMENT, len(string))
            self._vm_writer.write_call(self._STRING_CREATOR, 1)
            for char in string:
                self._vm_writer.write_push(self._CONST_SEGMENT, ord(char))
                self._vm_writer.write_call(self._STRING_APPENDER, 2)
            self._tokenizer.advance()
        elif self._tokenizer.value() in self._CONSTANT_LIST:
            if self._tokenizer.value() == self._THIS_STRING:
                self._vm_writer.write_push(self._POINTER_SEGMENT, 0)
            else:
                self._vm_writer.write_push(self._CONST_SEGMENT, 0)
                if self._tokenizer.value() == self._TRUE_STRING:
                    self._vm_writer.write_arithmetic(self._NOT_COMMAND)
            self._tokenizer.advance()  # Skip the constant
        elif self._tokenizer.value() in self._PRE_TERM_CONSTANT_LIST:
            op: str = self._tokenizer.value()
            self._tokenizer.advance()
            self._compile_term()
            self._vm_writer.write_arithmetic(self._NEGATION if op == self._UNARY_MINUS else self._NOT_COMMAND)
        elif self._tokenizer.value() == self._LEFT_PARENTHESIS:
            self._tokenizer.advance()  # Skip '('
            self._compile_expression()
            self._tokenizer.advance()  # Skip ')'
        else:
            name: str = self._tokenizer.value()
            self._tokenizer.advance()
            if self._tokenizer.value() == self._START_OF_EXPRESSION_INDEXING:
                # ---Handle the array indexing---
                self._tokenizer.advance()  # Skip '['
                self._compile_expression()  # Compute the index (i)
                self._tokenizer.advance()  # Skip ']'
                # Push the base address of the array
                self._vm_writer.write_push(self._symbol_table.kind_of(name), self._symbol_table.index_of(name))
                self._vm_writer.write_arithmetic(self._ADD_COMMAND)  # Add the index to the base address
                # Save the computed address in `that` (pointer 1)
                self._vm_writer.write_pop(self._POINTER_SEGMENT, 1)
                self._vm_writer.write_push(self._THAT_SEGMENT, 0)  # Push the value of the array element
            elif self._tokenizer.value() in self._START_OF_SUBROUTINE_CALL:
                start_value: int = 0
                if (kind := self._symbol_table.kind_of(name)) is not None:
                    self._vm_writer.write_push(kind, self._symbol_table.index_of(name))
                    name = self._symbol_table.type_of(name)
                    start_value += 1
                self._tokenizer.advance()  # Skip '(' or '.'
                self._compile_subroutine_call(name, start_value)
            else:
                self._vm_writer.write_push(self._symbol_table.kind_of(name), self._symbol_table.index_of(name))

    def _compile_expression_list(self, start_value: int = 0) -> int:
        """
        Compiles a (possibly empty) comma-separated list of expressions.
        :param start_value: The start value of the number of arguments.
        """
        n_args = start_value
        if self._tokenizer.value() != self._RIGHT_PARENTHESIS:
            self._compile_expression()
            n_args += 1
            while self._tokenizer.value() == self._COMMA:
                self._tokenizer.advance()  # Skip ','
                self._compile_expression()
                n_args += 1
        return n_args
