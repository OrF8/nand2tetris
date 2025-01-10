"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""

from typing import Dict, Optional, Union


class SymbolTable:
    """
    A symbol table that associates names with information needed for Jack
    compilation: type, kind and running index. The symbol table has two nested
    scopes (class/subroutine).
    """

    _STATIC = "static"
    _FIELD = "field"
    _ARG = "argument"
    _VAR = "var"
    _TYPE = "type"
    _KIND = "kind"
    _INDEX = "index"
    _THIS = "this"

    def __init__(self) -> None:
        """Creates a new empty symbol table."""
        self._class_scope: Dict[str, Dict[str, Union[str, int]]] = {}
        self._subroutine_scope: Dict[str, Dict[str, Union[str, int]]] = {}
        self.indexes: Dict[str, int] = {
            self._STATIC: 0,
            self._FIELD: 0,
            self._ARG: 0,
            self._VAR: 0
        }

    def start_subroutine(self, is_method: bool) -> None:
        """
        Starts a new subroutine scope (i.e., resets the subroutine's symbol table).

        :param is_method: True if the subroutine is a method, False otherwise.
        """
        self._subroutine_scope = {}
        self.indexes[self._ARG] = 1 if is_method else 0
        self.indexes[self._VAR] = 0

    def define(self, name: str, identifier_type: str, kind: str) -> None:
        """
        Defines a new identifier of a given name, type, and kind and assigns
        it a running index. "STATIC" and "FIELD" identifiers have a class scope, 
        while "ARG" and "VAR" identifiers have a subroutine scope.

        :param name: The name of the new identifier.
        :param identifier_type: The type of the new identifier.
        :param kind: The kind of the new identifier. It can be: "STATIC", "FIELD", "ARG" or "VAR".
        """
        if kind in [self._STATIC, self._FIELD]:
            self._class_scope[name] = {
                self._TYPE: identifier_type,
                self._KIND: kind,
                self._INDEX: self.indexes[kind]
            }
        else:
            self._subroutine_scope[name] = {
                self._TYPE: identifier_type,
                self._KIND: kind,
                self._INDEX: self.indexes[kind]
            }
        self.indexes[kind] += 1

    def var_count(self, kind: str) -> int:
        """
        :param kind: can be "STATIC", "FIELD", "ARG" or "VAR".
        :return: The number of variables of the given kind that are already defined in the current scope.
        """
        return sum(1 for identifier in self._class_scope.values() if identifier[self._KIND] == kind) + \
            sum(1 for identifier in self._subroutine_scope.values() if identifier[self._KIND] == kind)

    def kind_of(self, name: str) -> Optional[str]:
        """
        :param name: The name of an identifier.
        :return: The kind of the named identifier in the current scope,
                 or None if the identifier is unknown in the current scope.
        """
        if name == self._THIS:
            return self._FIELD
        if name in self._subroutine_scope:
            return self._subroutine_scope[name][self._KIND]
        if name in self._class_scope:
            return self._class_scope[name][self._KIND]
        return None

    def type_of(self, name: str) -> Optional[str]:
        """
        :param name: The name of an identifier.
        :return: The type of the named identifier in the current scope.
        """
        if name in self._subroutine_scope:
            return self._subroutine_scope[name][self._TYPE]
        if name in self._class_scope:
            return self._class_scope[name][self._TYPE]
        return None

    def index_of(self, name: str) -> int:
        """
        :param name: The name of an identifier.
        :return: The index assigned to the named identifier.
        """
        if name == self._THIS:
            return 0
        if name in self._subroutine_scope:
            return self._subroutine_scope[name][self._INDEX]
        if name in self._class_scope:
            return self._class_scope[name][self._INDEX]
        return -1
