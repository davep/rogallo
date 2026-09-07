"""Provides widgets for displaying Gemtext content."""

##############################################################################
# Python imports.
from typing import Final

##############################################################################
# Gemtext imports.
from gemtext import (
    Heading,
    Line,
    Link,
    ListItem,
    Paragraph,
    PreFormatted,
    Quote,
    SpartanPrompt,
)

##############################################################################
# Local imports.
from .content_filter import GemtextContent
from .heading import GemtextHeading
from .link import GemtextLink, SpartanPromptLink
from .list_item import GemtextListItem
from .paragraph import GemtextParagraph
from .preformatted import GemtextPreformatted
from .quote import GemtextQuote
from .searchable import Searchable
from .text import GemtextText

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
    SpartanPrompt: SpartanPromptLink,
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
    return _BLOCKS.get(type(line), GemtextParagraph)(line)


##############################################################################
# Exports.
__all__ = [
    "GemtextContent",
    "GemtextLink",
    "get_block_widget",
    "Searchable",
]

### __init__.py ends here
