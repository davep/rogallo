"""Provides a widget for displaying a Gemtext paragraph."""

##############################################################################
# Local imports.
from .text import GemtextText


##############################################################################
class GemtextParagraph(GemtextText):
    """A widget for displaying a Gemtext paragraph."""

    DEFAULT_CSS = """
    GemtextParagraph {
        padding: 0 2;
    }
    """


### paragraph.py ends here
