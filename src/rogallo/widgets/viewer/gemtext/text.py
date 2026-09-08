"""Provides the base widget for most forms of Gemtext text."""

##############################################################################
# Gemtext imports.
from gemtext import Line
from rich.text import Text

##############################################################################
# Textual imports.
from textual.content import Content
from textual.geometry import Region
from textual.style import Style
from textual.widgets import Static

##############################################################################
# Local imports.
from ..searchable import NEEDLE
from .content_filter import GemtextContent


##############################################################################
class GemtextText(Static):
    """A widget for displaying a block of Gemtext text."""

    COMPONENT_CLASSES = {NEEDLE}

    def __init__(
        self, line: Line | Content | Text | str, classes: str | None = None
    ) -> None:
        """Initialise the object.

        Args:
            line: The Gemtext line to display.
        """
        self._gemtext_content: Content
        """The content of the Gemtext line."""
        if isinstance(line, Content):
            self._gemtext_content = line
        elif isinstance(line, Text):
            self._gemtext_content = Content.from_rich_text(line)
        elif isinstance(line, str):
            self._gemtext_content = Content(line)
        else:
            if isinstance(line := GemtextContent.filter(line), Text):
                self._gemtext_content = Content.from_rich_text(line)
            else:
                self._gemtext_content = Content(line)
        self._find_state: int = -1
        """The current state of the search."""
        super().__init__(self._gemtext_content, markup=False, classes=classes)

    def find_reset(self) -> None:
        """Reset the search state of the widget."""
        self._find_state = -1
        self.update(self._gemtext_content)

    def find_next_text(self, needle: str) -> bool:
        """Find the next occurrence of the needle in the Gemtext text.

        Args:
            needle: The string to find.

        Returns:
            True if the needle was found, False otherwise.
        """
        self._find_state = self._gemtext_content.plain.casefold().find(
            needle.casefold(),
            self._find_state + 1 if self._find_state is not None else 0,
        )
        if self._find_state < 0:
            self.update(self._gemtext_content)
            return False
        self.update(
            self._gemtext_content.stylize(
                Style.combine(
                    (
                        Style.from_rich_style(self.get_component_rich_style(NEEDLE)),
                        Style.from_meta({NEEDLE: True}),
                    )
                ),
                self._find_state,
                self._find_state + len(needle),
            )
        )
        return True

    def found_region(self) -> Region:
        """Get the region of the found text in the widget.

        Returns:
            The region of the found text, or the widget's region.
        """
        if self._find_state < 0:
            return self.virtual_region_with_margin
        matching_lines: list[int] = []
        gather_match = matching_lines.append
        for y, line in enumerate(
            self.visual.to_strips(
                self, self.visual, self.size.width, self.size.height, Style()
            )
        ):
            for segment in line:
                if segment.style and segment.style.meta.get(NEEDLE) is True:
                    gather_match(y)
        return (
            Region(
                0,
                self.virtual_region_with_margin.y + matching_lines[0],
                self.size.width,
                max(1, len(matching_lines)),
            )
            if matching_lines
            else self.virtual_region_with_margin
        )


### text.py ends here
