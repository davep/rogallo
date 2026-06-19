"""The viewer widget for Rogallo."""

##############################################################################
# Python imports.
from typing import Final

##############################################################################
# Textual imports.
from textual.app import ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.reactive import var
from textual.widgets import Label, Static
from textual.widgets import Link as TextualLink

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
    GemtextListItem Label.--bullet {
        color: $text-primary;
        margin-right: 1;
        &:light {
            color: $text-secondary;
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
class GemtextLink(TextualLink):
    """A widget for displaying a Gemtext link."""

    def __init__(self, link: Line) -> None:
        """Initialize a Gemtext link widget.

        Args:
            line: The Gemtext link to display.
        """
        assert isinstance(link, Link)
        super().__init__(str(link), url=link.uri)


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

        &.--has-document {
            visibility: visible;
        }
    }
    """

    document: var[str] = var("", toggle_class="--has-document")
    """The document to display in the viewer."""

    _BLOCKS: Final[
        dict[
            type[Line],
            type[GemtextText | GemtextLink | GemtextListItem | GemtextPreformatted],
        ]
    ] = {
        Paragraph: GemtextText,
        ListItem: GemtextListItem,
        Quote: GemtextQuote,
        PreFormatted: GemtextPreformatted,
        Heading: GemtextHeading,
        Link: GemtextLink,
    }
    """Mapping of Gemtext line types to viewer block types."""

    async def _watch_document(self) -> None:
        """Watch for changes to the document and update the viewer."""
        await self.remove_children()
        await self.mount_all(
            self._BLOCKS[type(line)](line) for line in Gemtext(self.document).content
        )


### viewer.py ends here
