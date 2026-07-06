"""Search and visit bookmarks from the command palette."""

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import CommandHit, CommandHits, CommandsProvider

##############################################################################
# Local imports.
from ..data import Bookmarks
from ..messages import OpenLocation


##############################################################################
class BookmarkSearchCommands(CommandsProvider):
    """A command palette provider related to bookmarks."""

    bookmarks: Bookmarks = []
    """The bookmarks."""

    @classmethod
    def prompt(cls) -> str:
        """The prompt for the command provider."""
        return "Search bookmarks..."

    def commands(self) -> CommandHits:
        """Provide the bookmark-based command data for the command palette.

        Yields:
            The commands for the command palette.
        """
        for bookmark in sorted(self.bookmarks):
            yield CommandHit(
                f"Visit {bookmark.title}",
                f"{bookmark.location}",
                OpenLocation(bookmark.location),
            )


### bookmarks.py ends here
