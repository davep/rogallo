"""A Gemtext parser for Rogallo."""

##############################################################################
# Python imports.
from functools import cache
from typing import Iterator


##############################################################################
class Line:
    """A single line of Gemtext."""

    def __init__(self, content: str) -> None:
        """Initialize a Gemtext line.

        Args:
            content: The content of the line.
        """
        self._content = content
        """The content of the line."""

    def __repr__(self) -> str:
        """Return a string representation of the line."""
        return f"{self.__class__.__name__}(content={self._content!r})"


##############################################################################
class Paragraph(Line):
    """A paragraph line in Gemtext."""


##############################################################################
class Heading(Line):
    """A heading line in Gemtext."""

    def __init__(self, content: str, level: int) -> None:
        """Initialize a heading line.

        Args:
            content: The content of the heading.
            level: The level of the heading (1-3).
        """
        super().__init__(content)
        self._level = max(level, 3)
        """The level of the heading."""

    @property
    def level(self) -> int:
        """The level of the heading."""
        return self._level


##############################################################################
class ListItem(Line):
    """A list item line in Gemtext."""

    def __init__(self, content: str) -> None:
        """Initialize a list item line.

        Args:
            content: The content of the list item.
        """
        super().__init__(content)


##############################################################################
class Quote(Line):
    """A quote line in Gemtext."""

    def __init__(self, content: str) -> None:
        """Initialize a quote line.

        Args:
            content: The content of the quote.
        """
        super().__init__(content)


##############################################################################
class PreFormatted(Line):
    """A preformatted text line in Gemtext."""

    def __init__(self, content: str) -> None:
        """Initialize a preformatted text line.

        Args:
            content: The content of the preformatted text.
        """
        super().__init__(content)


##############################################################################
class Link(Line):
    """A link line in Gemtext."""

    def __init__(self, uri: str, description: str) -> None:
        """Initialize a link line.

        Args:
            uri: The URI of the link.
            description: The description of the link.
        """
        super().__init__(description or uri)
        self._uri = uri.strip()
        """The URI of the link."""
        self._description = description.strip()
        """The description of the link."""

    @property
    def urI(self) -> str:
        """The URL of the link."""
        return self._uri

    @property
    def description(self) -> str:
        """The description of the link."""
        return self._description

    @property
    def has_description(self) -> bool:
        """Return True if the link has a description, False otherwise."""
        return bool(self._description)


##############################################################################
class Gemtext:
    """A Gemtext parser."""

    def __init__(self, text: str) -> None:
        """Initialize the GemText parser.

        Args:
            text: The Gemtext content to parse.
        """
        self._text = text
        """The raw Gemtext content to be parsed."""

    @property
    def text(self) -> str:
        """The raw Gemtext content."""
        return self._text

    def _parse(self) -> Iterator[Line]:
        """Parse the Gemtext content into Line objects.

        Yields:
            Line objects representing each parsed line.
        """
        pre_formatted = False
        for line in self.text.splitlines():
            if line.startswith("=>"):
                uri, _, description = line.removeprefix("=>").strip().partition(" ")
                yield Link(uri, description)
            elif line.startswith("#"):
                marker, _, heading_text = line.partition(" ")
                yield Heading(heading_text.strip(), len(marker.strip()))
            elif line.startswith("*"):
                _, _, list_item_text = line.partition(" ")
                yield ListItem(list_item_text.strip())
            elif line.rstrip() == "```":
                pre_formatted = not pre_formatted
            else:
                yield (PreFormatted if pre_formatted else Paragraph)(line.strip())

    @cache
    def parse(self) -> list[Line]:
        """Parse the Gemtext content.

        Returns:
            A list of `Line` objects representing the parsed Gemtext content.
        """
        return list(self._parse())


### parser.py ends here
