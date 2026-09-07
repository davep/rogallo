"""Provides a widget for displaying a Gemtext quote."""

##############################################################################
# Local imports.
from .text import GemtextText


##############################################################################
class GemtextQuote(GemtextText):
    """A widget for displaying a Gemtext quote."""

    DEFAULT_CSS = """
    GemtextQuote {
        background: $boost;
        border-left: outer $text-primary 50%;
        padding: 0 1;
        &:light {
            border-left: outer $text-secondary;
        }
    }
    """


### quote.py ends here
