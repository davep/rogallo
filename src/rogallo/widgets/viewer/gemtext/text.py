"""Provides the base widget for most forms of Gemtext text."""

##############################################################################
# Gemtext imports.
from gemtext import Line
from rich.text import Text

##############################################################################
# Textual imports.
from textual.content import Content

##############################################################################
# Local imports.
from ..plain_text import PlainText
from .content_filter import GemtextContent


##############################################################################
class GemtextText(PlainText):
    """A widget for displaying a block of Gemtext text."""

    def __init__(
        self, line: Line | Content | Text | str, classes: str | None = None
    ) -> None:
        """Initialise the object.

        Args:
            line: The Gemtext line to display.
        """
        if isinstance(line, Line):
            line = GemtextContent.filter(line)
        super().__init__(line, classes=classes)


### text.py ends here
