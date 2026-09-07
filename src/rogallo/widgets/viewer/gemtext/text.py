"""Provides the base widget for most forms of Gemtext text."""

##############################################################################
# Gemtext imports.
from gemtext import Line
from rich.text import Text

##############################################################################
# Textual imports.
from textual.content import Content
from textual.widgets import Static

##############################################################################
# Local imports.
from .content_filter import GemtextContent


##############################################################################
class GemtextText(Static):
    """A widget for displaying a block of Gemtext text."""

    def __init__(
        self, line: Line | Content | Text | str, classes: str | None = None
    ) -> None:
        """Initialise the object.

        Args:
            line: The Gemtext line to display.
        """
        super().__init__(
            GemtextContent.filter(line) if isinstance(line, Line) else line,
            markup=False,
            classes=classes,
        )


### text.py ends here
