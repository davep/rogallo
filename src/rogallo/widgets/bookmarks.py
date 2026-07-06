"""Provides the bookmarks panel widget."""

##############################################################################
# Rich imports.
from rich.markup import escape

##############################################################################
# Textual imports.
from textual.reactive import var
from textual.widgets.option_list import Option

##############################################################################
# Textual enhanced imports.
from textual_enhanced.widgets import EnhancedOptionList

##############################################################################
# Local imports.
from ..data.bookmarks import Bookmark, Bookmarks
from ..types import short_location


##############################################################################
class BookmarkOption(Option):
    """An option for the bookmarks viewer."""

    def __init__(self, bookmark: Bookmark) -> None:
        """Initialise the bookmark option.

        Args:
            bookmark: The bookmark to display.
            index: The index of the bookmark in the list.
        """
        super().__init__(
            (
                f"{escape(bookmark.title)}\n"
                f"[dim]{escape(short_location(bookmark.location))}[/]"
            ),
            id=str(bookmark.location),
        )
        self._bookmark = bookmark
        """The bookmark to display."""

    @property
    def bookmark(self) -> Bookmark:
        """The bookmark associated with this option."""
        return self._bookmark


##############################################################################
class BookmarksViewer(EnhancedOptionList):
    """A widget for displaying the bookmarks."""

    DEFAULT_CSS = """
    BookmarksViewer {
        height: 1fr;
        border: none;
        text-wrap: nowrap;
        text-overflow: ellipsis;
        &:focus {
            border: none;
            background: $panel;
        }
    }
    """

    HELP = """
    ## Bookmarks

    These are your bookmarks. Here you can revisit locations you've saved,
    and also manage the bookmarks.
    """

    bookmarks: var[Bookmarks] = var(list)
    """The bookmarks to display."""

    def _watch_bookmarks(self) -> None:
        """React to the bookmarks changing."""
        self.clear_options().add_options(
            [BookmarkOption(bookmark) for bookmark in self.bookmarks]
        )
        if self.option_count:
            self.highlighted = 0


### bookmarks.py ends here
