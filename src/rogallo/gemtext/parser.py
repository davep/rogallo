"""A Gemtext parser for Rogallo."""

##############################################################################
# Python imports.
from collections.abc import Iterator
from functools import cached_property


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

    def __str__(self) -> str:
        """Return the content of the line as a string."""
        return self._content

    def __repr__(self) -> str:
        """Return a string representation of the line."""
        return f"{self.__class__.__name__}(content={self._content!r})"


##############################################################################
class Paragraph(Line):
    """A paragraph line in Gemtext."""


##############################################################################
class ListItem(Line):
    """A list item line in Gemtext."""


##############################################################################
class Quote(Line):
    """A quote line in Gemtext."""


##############################################################################
class PreFormatted(Line):
    """A preformatted text line in Gemtext."""


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
        self._level = level
        """The level of the heading."""

    @property
    def level(self) -> int:
        """The level of the heading."""
        return self._level


##############################################################################
class Link(Line):
    """A link line in Gemtext."""

    def __init__(self, uri: str, description: str) -> None:
        """Initialize a link line.

        Args:
            uri: The URI of the link.
            description: The description of the link.
        """
        self._uri = uri.strip()
        """The description of the link."""
        super().__init__(description.strip() or self._uri)

    @property
    def uri(self) -> str:
        """The URI of the link."""
        return self._uri


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

    def _parse(self) -> Iterator[Line]:
        """Parse the Gemtext content into Line objects.

        Yields:
            Line objects representing each parsed line.
        """
        in_preformat = False
        preformat_content: list[str] = []
        for line in self._text.splitlines():
            if line.startswith("```"):
                if not (in_preformat := not in_preformat):
                    yield PreFormatted("\n".join(preformat_content))
                    preformat_content = []
            elif in_preformat:
                preformat_content.append(line)
            elif line.startswith("=> "):
                parts = line.removeprefix("=>").strip().split(maxsplit=1)
                yield Link(parts[0], parts[1] if len(parts) > 1 else "")
            elif line.startswith("> "):
                _, _, quote_text = line.partition(" ")
                yield Quote(quote_text.strip())
            elif line.startswith(("# ", "## ", "### ")):
                marker, _, heading_text = line.partition(" ")
                yield Heading(heading_text.strip(), len(marker.strip()))
            elif line.startswith("* "):
                _, _, list_item_text = line.partition(" ")
                yield ListItem(list_item_text.strip())
            else:
                yield Paragraph(line)
        if in_preformat:
            yield PreFormatted("\n".join(preformat_content))

    @cached_property
    def content(self) -> tuple[Line, ...]:
        """The content of the Gemtext."""
        return tuple(self._parse())

    def __str__(self) -> str:
        """Return the Gemtext content as a string."""
        return self._text


### parser.py ends here
