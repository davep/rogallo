"""Provides a widget for displaying a Gemtext list item."""

##############################################################################
# Gemtext imports.
from gemtext import Line

##############################################################################
# Rich imports.
from rich.table import Table
from rich.text import Text

##############################################################################
# Textual imports.
from textual.selection import Selection
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
        super().__init__()
        self._bullet = icon("list_item_bullet_icon")
        """The bullet icon for the Gemtext list item."""
        self._list_item = list_item
        """The Gemtext list item to display."""
        self._text = GemtextContent.filter(list_item)
        """The text content of the Gemtext list item."""

    def render(self) -> Table:
        """Render the Gemtext list item widget."""
        text = Text(self._text) if isinstance(self._text, str) else self._text.copy()
        if self.text_selection:
            text.stylize(
                self.screen.get_component_rich_style("screen--selection", partial=True)
            )
        item = Table.grid(expand=True)
        item.add_column(width=2, no_wrap=True)
        item.add_column(ratio=1, no_wrap=False)
        item.add_row(
            Text(
                self._bullet,
                style=self.get_component_rich_style("gemtext-list-item--bullet"),
            ),
            text,
        )
        return item

    def get_selection(self, selection: Selection) -> tuple[str, str] | None:
        return selection.extract(f"* {self._list_item}"), "\n"


### list_item.py ends here
