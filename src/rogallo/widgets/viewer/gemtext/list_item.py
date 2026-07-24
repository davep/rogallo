"""Provides a widget for displaying a Gemtext list item."""

##############################################################################
# Gemtext imports.
from gemtext import Line, ListItem

##############################################################################
# Textual imports.
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Label

##############################################################################
# Local imports.
from .content_filter import GemtextContent
from .icons import icon


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
        yield Label(icon("list_item_bullet_icon"), id="bullet")
        yield Label(
            GemtextContent.filter(self._list_item), markup=False, shrink=True, id="text"
        )


### list_item.py ends here
