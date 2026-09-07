"""Provides the base widget for most forms of Gemtext text."""

##############################################################################
# Gemtext imports.
from gemtext import Line
from rich.text import Text

##############################################################################
# Textual imports.
from textual.content import Content
from textual.style import Style
from textual.widgets import Static


##############################################################################
class GemtextText(Static):
    """A widget for displaying a block of Gemtext text."""

    COMPONENT_CLASSES = {"gemtext--needle"}

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
        else:
            self._gemtext_content = Content(str(line))
        self._find_state: int = -1
        """The current state of the search."""
        super().__init__(self._gemtext_content, markup=False, classes=classes)

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
        self.set_class(self._find_state >= 0, "--contains-search-hit")
        if self._find_state < 0:
            self.update(self._gemtext_content)
            return False
        self.update(
            self._gemtext_content.stylize(
                Style.from_rich_style(self.get_component_rich_style("gemtext--needle")),
                self._find_state,
                self._find_state + len(needle),
            )
        )
        return True


### text.py ends here
