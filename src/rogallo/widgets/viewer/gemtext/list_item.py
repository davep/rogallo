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
from textual.geometry import Region
from textual.selection import Selection
from textual.widget import Widget

##############################################################################
# Local imports.
from .content_filter import GemtextContent
from .icons import icon
from .searchable import NEEDLE


##############################################################################
class GemtextListItem(Widget):
    """A widget for displaying a Gemtext list item."""

    COMPONENT_CLASSES = {"gemtext-list-item--bullet", NEEDLE}

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
        self._find_state: int = -1
        """The current state of the search."""
        self._needle: str | None = None
        """The current search needle."""

    def find_reset(self) -> None:
        """Reset the search state of the widget."""
        self._find_state = -1
        self._needle = None
        self.refresh()

    def render(self) -> Table:
        """Render the Gemtext list item widget."""
        text = Text(self._text) if isinstance(self._text, str) else self._text.copy()
        if self.text_selection:
            text.stylize(
                self.screen.get_component_rich_style("screen--selection", partial=True)
            )
        if self._needle and self._find_state >= 0:
            text.stylize(
                self.get_component_rich_style(NEEDLE),
                self._find_state,
                self._find_state + len(self._needle),
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

    def find_next_text(self, needle: str) -> bool:
        """Find the next occurrence of the needle in the Gemtext list item.

        Args:
            needle: The string to find.

        Returns:
            True if the needle was found, False otherwise.
        """
        self._needle = needle
        self._find_state = (
            (Text(self._text) if isinstance(self._text, str) else self._text.copy())
            .plain.casefold()
            .find(
                needle.casefold(),
                self._find_state + 1 if self._find_state is not None else 0,
            )
        )
        self.refresh()
        return self._find_state >= 0

    def found_region(self) -> Region:
        """Get the region of the found text in the widget.

        Returns:
            The region of the found text, or the widget's region.
        """
        return self.virtual_region_with_margin

    def get_selection(self, selection: Selection) -> tuple[str, str] | None:
        return selection.extract(f"* {self._list_item}"), "\n"


### list_item.py ends here
