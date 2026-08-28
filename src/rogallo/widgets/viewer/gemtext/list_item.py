"""Provides a widget for displaying a Gemtext list item."""

##############################################################################
# Gemtext imports.
from gemtext import Line, ListItem

##############################################################################
# Rich imports.
from rich.table import Table
from rich.text import Text

##############################################################################
# Textual imports.
from textual.widget import Widget

##############################################################################
# Local imports.
from .content_filter import GemtextContent
from .icons import icon


##############################################################################
class GemtextListItem(Widget):
    """A widget for displaying a Gemtext list item."""

    COMPONENT_CLASSES = {"gemtext-list-item--bullet"}

    DEFAULT_CSS = """
    GemtextListItem {
        margin: 0 2 0 0;
        height: auto;

        & > .gemtext-list-item--bullet {
            color: $text-primary;
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
        """The Gemtext list item to display."""

    def render(self) -> Table:
        """Render the Gemtext list item widget."""
        item = Table.grid(expand=True)
        item.add_column(width=2, no_wrap=True)
        item.add_column(ratio=1, no_wrap=False)
        item.add_row(
            Text(
                icon("list_item_bullet_icon"),
                style=self.get_component_rich_style("gemtext-list-item--bullet"),
            ),
            GemtextContent.filter(self._list_item),
        )
        return item


### list_item.py ends here
