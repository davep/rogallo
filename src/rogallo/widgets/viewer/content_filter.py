"""Provides a configurable content filter."""

##############################################################################
# Python imports.
from unicodedata import category

##############################################################################
# BagOfStuff imports.
from bagofstuff.pipe import Pipe

##############################################################################
# Gemtext imports.
from gemtext import Line

##############################################################################
# Rich imports.
from rich.text import Text

##############################################################################
type ContentFilter = Pipe[Line, str | Text]
"""A type for a content filter."""


##############################################################################
def _strip_emoji(text: str) -> str:
    """Strip emoji from a string.

    Args:
        text: The string to strip emoji from.

    Returns:
        The string with emoji stripped.
    """
    return "".join(char for char in text if category(char) != "So")


##############################################################################
class GemtextContent:
    """A class for filtering gemtext content."""

    _filter: ContentFilter = Pipe[Line, str | Text](str)
    """The content filter."""

    @staticmethod
    def _strip_ansi(text: str) -> str:
        """Strip ANSI escape sequences from a string.

        Args:
            text: The string to strip ANSI escape sequences from.
        """
        return Text.from_ansi(text).plain

    @classmethod
    def set_filter(
        cls, *, allow_ansi_escape_sequences: bool, strip_emoji: bool
    ) -> None:
        """Set the content filter.

        Args:
            allow_ansi_escape_sequences: Whether to allow ANSI escape sequences.
            strip_emoji: Whether to strip emoji from the content.
        """
        cls._filter = Pipe[Line, str | Text](str)
        if strip_emoji:
            cls._filter |= _strip_emoji
        if allow_ansi_escape_sequences:
            cls._filter |= Text.from_ansi
        else:
            cls._filter |= cls._strip_ansi

    @classmethod
    def filter(cls, line: Line) -> str | Text:
        """Filter a Gemtext line.

        Returns:
            The filtered line content.
        """
        return cls._filter(line)


### content_filter.py ends here
