"""The viewer widget for Rogallo."""

##############################################################################
# Python imports.
from typing import Final, NamedTuple
from urllib.parse import urlparse

##############################################################################
# Textual imports.
from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, VerticalScroll
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
from ...gemtext import (
    Gemtext,
    Heading,
    Line,
    Link,
    ListItem,
    Paragraph,
    PreFormatted,
    Quote,
)
from ..messages import OpenURI
from ..preflight import is_likely_capsule
from ..types import GeminiLocation


##############################################################################
class GemtextText(Static):
    """A widget for displaying a block of Gemtext text."""

    def __init__(self, line: Line) -> None:
        """Initialize a Gemtext widget.

        Args:
            line: The Gemtext line to display.
        """
        super().__init__(str(line))


##############################################################################
class GemtextParagraph(GemtextText):
    """A widget for displaying a Gemtext paragraph."""

    DEFAULT_CSS = """
    GemtextParagraph {
        padding: 0 2 0 2;
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
        padding: 0 2 0 0;
        Label.--bullet {
            color: $text-primary;
            margin-right: 1;
            &:light {
                color: $text-secondary;
            }
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
        yield Label("•", classes="--bullet")
        yield Label(str(self._list_item))


##############################################################################
class GemtextLink(Static, can_focus=True):
    """A widget for displaying a Gemtext link."""

    DEFAULT_CSS = """
    GemtextLink {
        width: auto;
        height: auto;
        min-height: 1;
        padding: 0;
        &:hover {
            background: $block-hover-background;
        }
        &:focus {
            color: $foreground;
            background: $block-cursor-blurred-background;
        }
        pointer: pointer;
    }
    """

    BINDINGS = [HelpfulBinding("enter", "open_link", "Open link", show=False)]

    def __init__(self, link: Line) -> None:
        """Initialize a Gemtext link widget.

        Args:
            line: The Gemtext link to display.
        """
        assert isinstance(link, Link)
        icon = "⪢" if is_likely_capsule(link.uri) else "↗"
        super().__init__(f"[$text-primary]{icon}[/] [u]{link}[/]")
        self._uri = link.uri
        """The URI of the link."""

    def normalise_uri(self, base_uri: GeminiLocation | None) -> None:
        """Normalise the URI of the link against a base URI.

        Args:
            base_uri: The base URI to normalise against.
        """
        if base_uri is None:
            return
        if urlparse(self._uri).scheme:
            return
        if isinstance(base_uri, GeminiURI):
            self._uri = str(base_uri.resolve(self._uri))

    @on(Click)
    def _action_open_link(self) -> None:
        """Open the link."""
        self.post_message(OpenURI(self._uri))


##############################################################################
class GemtextQuote(GemtextText):
    """A widget for displaying a Gemtext quote."""

    DEFAULT_CSS = """
    GemtextQuote {
        background: $boost;
        border-left: outer $text-primary 50%;
        margin: 1 0;
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
        background: $boost;
        overflow: auto;
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
        yield Label(str(self._preformatted))


##############################################################################
class Viewer(VerticalScroll):
    """The viewer widget for Rogallo."""

    DEFAULT_CSS = """
    Viewer {
        height: 1fr;
        width: 1fr;
        visibility: hidden;

        &.--has-content {
            visibility: visible;
        }
    }
    """

    class Document(NamedTuple):
        """A named tuple representing details of the document."""

        location: GeminiLocation | None
        """The source of the document."""
        content: str
        """The content of the document."""

        def __bool__(self) -> bool:
            """Return True if the document has content, False otherwise."""
            return bool(self.content)

    document: var[Document] = var(Document(None, ""), toggle_class="--has-content")
    """The details of the document to show in the viewer."""

    _content: var[str] = var("")
    """The content to display in the viewer."""
    _location: var[GeminiLocation | None] = var(None)
    """The location of the document on display in the viewer."""

    _BLOCKS: Final[
        dict[
            type[Line],
            type[GemtextText | GemtextLink | GemtextListItem | GemtextPreformatted],
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

    async def _watch_document(self) -> None:
        """Watch for changes to the document and update the viewer."""
        self._location = self.document.location
        self._content = self.document.content
        await self.remove_children()
        for widget in (
            blocks := [
                self._BLOCKS[type(line)](line)
                for line in Gemtext(self._content).content
            ]
        ):
            if isinstance(widget, GemtextLink):
                widget.normalise_uri(self._location)
        await self.mount_all(blocks)


### viewer.py ends here
