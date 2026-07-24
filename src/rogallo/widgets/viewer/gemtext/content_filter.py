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
class ContentFilter(Pipe[Line, str | Text]):
    """The content filtering pipeline."""


##############################################################################
class GemtextContent:
    """A class for filtering gemtext content."""

    _filter: ContentFilter = ContentFilter(str)
    """The content filter."""
    _purely_ansi_filter: ContentFilter = ContentFilter(str)
    """A content filter that only deals with ANSI escape sequences."""

    @staticmethod
    def _strip_ansi(text: str) -> str:
        """Strip ANSI escape sequences from a string.

        Args:
            text: The string to strip ANSI escape sequences from.

        Returns:
            The string with ANSI escape sequences stripped.
        """
        return Text.from_ansi(text).plain

    @staticmethod
    def _strip_emoji(text: str) -> str:
        """Strip emoji from a string.

        Args:
            text: The string to strip emoji from.

        Returns:
            The string with emoji stripped.
        """
        return "".join(char for char in text if category(char) != "So")

    @classmethod
    def set_filter(
        cls, *, allow_ansi_escape_sequences: bool, strip_emoji: bool
    ) -> None:
        """Set the content filter.

        Args:
            allow_ansi_escape_sequences: Whether to allow ANSI escape sequences.
            strip_emoji: Whether to strip emoji from the content.
        """
        cls._filter = ContentFilter(str)
        cls._purely_ansi_filter = ContentFilter(str)
        if strip_emoji:
            cls._filter |= cls._strip_emoji
        if allow_ansi_escape_sequences:
            cls._filter |= Text.from_ansi
            cls._purely_ansi_filter |= Text.from_ansi
        else:
            cls._filter |= cls._strip_ansi
            cls._purely_ansi_filter |= cls._strip_ansi

    @classmethod
    def filter(cls, line: Line) -> str | Text:
        """Filter a Gemtext line.

        Returns:
            The filtered line content.
        """
        return cls._filter(line)

    @classmethod
    def ansi_filter(cls, line: Line) -> str | Text:
        """Filter a Gemtext line, affecting only ANSI escape sequences.

        Returns:
            The filtered line content.
        """
        return cls._purely_ansi_filter(line)


### content_filter.py ends here
