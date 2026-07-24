"""Provides widgets for displaying Gemtext content."""

##############################################################################
# Python imports.
from typing import Final

##############################################################################
# Gemtext imports.
from gemtext import Heading, Line, Link, ListItem, Paragraph, PreFormatted, Quote

from .content_filter import GemtextContent
from .link import GemtextLink
from .list_item import GemtextListItem
from .preformatted import GemtextPreformatted

##############################################################################
# Local imports.
from .text import GemtextHeading, GemtextParagraph, GemtextQuote, GemtextText

##############################################################################
type GemtextWidget = GemtextText | GemtextLink | GemtextListItem | GemtextPreformatted
"""Type of a widget for displaying Gemtext."""

##############################################################################
_BLOCKS: Final[
    dict[
        type[Line],
        type[GemtextWidget],
    ]
] = {
    Paragraph: GemtextParagraph,
    ListItem: GemtextListItem,
    Quote: GemtextQuote,
    PreFormatted: GemtextPreformatted,
    Heading: GemtextHeading,
    Link: GemtextLink,
}
"""Mapping of Gemtext line types to viewer block types."""


##############################################################################
def get_block_widget(line: Line) -> GemtextWidget:
    """Get the widget class for a given Gemtext line.

    Args:
        line: The Gemtext line to get the widget class for.

    Returns:
        The widget class for the given Gemtext line.
    """
    return _BLOCKS[type(line)](line)


##############################################################################
# Exports.
__all__ = [
    "GemtextContent",
    "GemtextLink",
    "get_block_widget",
]

### __init__.py ends here
