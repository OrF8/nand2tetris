"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""

from bigvars import DEST_SWITCHER, COMP_SWITCHER, JUMP_SWITCHER, COMP_EXTENDED_SWITCHER


class Code:
    """Translates Hack assembly language mnemonics into binary codes."""

    @staticmethod
    def dest(mnemonic: str) -> str:
        """
        Args:
            mnemonic (str): a dest mnemonic string.

        Returns:
            str: 3-bit long binary code of the given mnemonic.
        """
        return DEST_SWITCHER.get(mnemonic, "000")

    @staticmethod
    def comp(mnemonic: str, is_extended: bool = False) -> str:
        """
        Args:
            mnemonic (str): a comp mnemonic string.
            is_extended (bool): a boolean value to check if the mnemonic is extended.

        Returns:
            str: the binary code of the given mnemonic.
        """
        if is_extended:
            return COMP_EXTENDED_SWITCHER.get(mnemonic, "0000000")
        return COMP_SWITCHER.get(mnemonic, "0000000")

    @staticmethod
    def jump(mnemonic: str) -> str:
        """
        Args:
            mnemonic (str): a jump mnemonic string.

        Returns:
            str: 3-bit long binary code of the given mnemonic.
        """
        return JUMP_SWITCHER.get(mnemonic, "000")
