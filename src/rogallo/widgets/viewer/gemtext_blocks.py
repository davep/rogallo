"""Provides widgets for showing Gemtext content."""

##############################################################################
# Python imports.
from collections.abc import Callable
from functools import cache
from pathlib import Path
from typing import Final
from urllib.parse import urlparse

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
)

##############################################################################
# Rich imports.
from rich.text import Text

##############################################################################
# Textual imports.
from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.events import Click
from textual.reactive import var
from textual.widgets import Label, Static

##############################################################################
# Textual enhanced imports.
from textual_enhanced.binding import HelpfulBinding

##############################################################################
# Wasat imports.
from wasat import GeminiURI

##############################################################################
# Local imports.
from ...data import load_configuration
from ...messages import OpenURI
from ...preflight import is_likely_capsule
from ...types import GeminiLocation


##############################################################################
@cache
def line_filter() -> Callable[[Line], str | Text]:
    """Get a filter function for Gemtext lines.

    Returns:
        A function that takes a Gemtext line and returns a string or Text
        object.
    """
    return (
        (lambda line: Text.from_ansi(str(line)))
        if load_configuration().handle_ansi_escape_sequences
        else str
    )


##############################################################################
class GemtextText(Static):
    """A widget for displaying a block of Gemtext text."""

    def __init__(self, line: Line) -> None:
        """Initialize a Gemtext widget.

        Args:
            line: The Gemtext line to display.
        """
        super().__init__(line_filter()(line), markup=False)


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
class GemtextListItem(Horizontal):
    """A widget for displaying a Gemtext list item."""

    DEFAULT_CSS = """
    GemtextListItem {
        margin: 0 2 0 0;
        height: auto;

        #bullet {
            color: $text-primary;
            padding-right: 1;
            &:light {
                color: $text-secondary;
            }
        }

        #text {
            margin-right: 2;
        }
    }
    """

    def __init__(self, list_item: Line) -> None:
        """Initialise a Gemtext list item widget.

        Args:
            list_item: The Gemtext list item to display.
        """
        assert isinstance(list_item, ListItem)
        super().__init__()
        self._list_item: ListItem = list_item

    def compose(self) -> ComposeResult:
        """Compose the Gemtext list item widget."""
        yield Label("•", id="bullet")
        yield Label(
            line_filter()(self._list_item), markup=False, shrink=True, id="text"
        )


##############################################################################
class GemtextLink(Horizontal, can_focus=True):
    """A widget for displaying a Gemtext link."""

    DEFAULT_CSS = """
    GemtextLink {
        margin: 0 2 0 0;
        height: auto;
        pointer: pointer;

        #icon {
            color: $text-primary;
            margin-right: 1;
            height: auto;
        }

        #text {
            margin-right: 2;
        }

        &:hover #text, #text:hover {
            background: $block-hover-background;
        }

        &:focus #text {
            color: $block-cursor-foreground;
            background: $block-cursor-background;
        }
    }
    """

    HELP = """
    ## Link

    This is a link to either another Gemini document, or an external
    resource that will be handled by your system.
    """

    BINDINGS = [HelpfulBinding("enter", "open_link", "Open link", show=False)]

    _normalised_uri: var[str] = var("")
    """The normalised URI to use when opening the link."""

    def __init__(self, link: Line) -> None:
        """Initialize a Gemtext link widget.

        Args:
            line: The Gemtext link to display.
        """
        super().__init__()
        assert isinstance(link, Link)
        self._icon = "⪢" if is_likely_capsule(link.uri) else "↗"
        """The icon to display for the link."""
        self._link = link
        """The link data."""
        self._normalised_uri = link.uri
        """The normalised URI to use when opening the link."""

    @property
    def normalised_uri(self) -> str:
        """The normalised URI to use when opening the link."""
        return self._normalised_uri

    def normalise_uri(self, base_uri: GeminiLocation | None) -> None:
        """Normalise the URI of the link against a base URI.

        Args:
            base_uri: The base URI to normalise against.
        """
        if base_uri is None:
            return
        if urlparse(self._normalised_uri).scheme:
            return
        if isinstance(base_uri, GeminiURI):
            self._normalised_uri = str(base_uri.resolve(self._link.uri))
        elif isinstance(base_uri, Path):
            self._normalised_uri = (base_uri.parent / self._link.uri).resolve().as_uri()

    def _watch__normalised_uri(self) -> None:
        """Watch for changes to the normalised URI."""
        if load_configuration().show_link_tooltips:
            self.tooltip = self._normalised_uri

    def compose(self) -> ComposeResult:
        """Compose the Gemtext link widget."""
        yield Label(self._icon, id="icon")
        yield Label(line_filter()(self._link), id="text", markup=False, shrink=True)

    @on(Click)
    def _action_open_link(self) -> None:
        """Open the link."""
        self.post_message(OpenURI(self._normalised_uri, allow_cached=False))


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


##############################################################################
class GemtextPreformatted(Static):
    """A widget for displaying a Gemtext preformatted text block."""

    DEFAULT_CSS = """
    GemtextPreformatted {
        margin: 0 2;
        background: black 35%;
        overflow: auto;
        &:light {
            background: white 35%;
        }
    }
    """

    def __init__(self, preformatted: Line) -> None:
        """Initialize a Gemtext preformatted text widget.

        Args:
            preformatted: The Gemtext preformatted text to display.
        """
        assert isinstance(preformatted, PreFormatted)
        self._preformatted = preformatted
        super().__init__()

    def compose(self) -> ComposeResult:
        """Compose the Gemtext preformatted text widget."""
        yield Label(line_filter()(self._preformatted), markup=False)


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


### gemtext_blocks.py ends here
