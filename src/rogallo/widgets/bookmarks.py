"""Provides the bookmarks panel widget."""

##############################################################################
# Textual imports.
from textual.reactive import var

##############################################################################
# Textual enhanced imports.
from textual_enhanced.widgets import EnhancedOptionList

##############################################################################
# Local imports.
from ..data.bookmarks import Bookmarks


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
            [bookmark.title for bookmark in self.bookmarks]
        )
        if self.option_count:
            self.highlighted = 0


### bookmarks.py ends here
