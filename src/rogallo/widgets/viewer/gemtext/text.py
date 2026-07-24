"""Provides widgets that display plain text type content."""

##############################################################################
# Gemtext imports.
from gemtext import Heading, Line

##############################################################################
# Textual imports.
from textual.widgets import Static

##############################################################################
# Local imports.
from .content_filter import GemtextContent


##############################################################################
class GemtextText(Static):
    """A widget for displaying a block of Gemtext text."""

    def __init__(self, line: Line) -> None:
        """Initialize a Gemtext widget.

        Args:
            line: The Gemtext line to display.
        """
        super().__init__(GemtextContent.filter(line), markup=False)


##############################################################################
class GemtextParagraph(GemtextText):
    """A widget for displaying a Gemtext paragraph."""

    DEFAULT_CSS = """
    GemtextParagraph {
        padding: 0 2;
    }
    """


##############################################################################
class GemtextHeading(GemtextText):
    """A widget for displaying a Gemtext heading."""

    DEFAULT_CSS = """
    GemtextHeading {
        padding: 1 0;
        &.--heading-1 {
            color: $markdown-h1-color;
            background: $markdown-h1-background;
            text-style: $markdown-h1-text-style;
            text-align: center;
        }
        &.--heading-2 {
            color: $markdown-h2-color;
            background: $markdown-h2-background;
            text-style: $markdown-h2-text-style;
        }
        &.--heading-3 {
            color: $markdown-h3-color;
            background: $markdown-h3-background;
            text-style: $markdown-h3-text-style;
        }
    }
    """

    def __init__(self, heading: Line) -> None:
        """Initialize a Gemtext heading widget.

        Args:
            heading: The Gemtext heading to display.
        """
        super().__init__(heading)
        assert isinstance(heading, Heading)
        self.add_class(f"--heading-{heading.level}")


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


### text.py ends here
