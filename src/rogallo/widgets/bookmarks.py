"""Provides the bookmarks panel widget."""

##############################################################################
# Python future imports.
from __future__ import annotations

##############################################################################
# Python imports.
from dataclasses import dataclass

##############################################################################
# Textual imports.
from textual import on, work
from textual.message import Message
from textual.reactive import var
from textual.widgets.option_list import Option

##############################################################################
# Textual enhanced imports.
from textual_enhanced.binding import HelpfulBinding
from textual_enhanced.dialogs import Confirm, ModalInput
from textual_enhanced.widgets import EnhancedOptionList

##############################################################################
# Local imports.
from ..data.bookmarks import Bookmark, Bookmarks
from ..messages import OpenLocation
from ..safe_escape import escape
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
                f"[dim i]{escape(short_location(bookmark.location))}[/]"
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

    BINDINGS = [
        HelpfulBinding(
            "r", "rename", "Rename", show=True, tooltip="Rename the selected bookmark"
        ),
        HelpfulBinding(
            "d", "delete", "Delete", show=True, tooltip="Delete the selected bookmark"
        ),
    ]

    bookmarks: var[Bookmarks] = var(list)
    """The bookmarks to display."""

    def _watch_bookmarks(self) -> None:
        """React to the bookmarks changing."""
        self.clear_options().add_options(
            [BookmarkOption(bookmark) for bookmark in sorted(self.bookmarks)]
        )
        if self.option_count:
            self.highlighted = 0

    @on(EnhancedOptionList.OptionSelected)
    def _jump_to_bookmark(self, event: EnhancedOptionList.OptionSelected) -> None:
        """Jump to the selected bookmark."""
        event.stop()
        assert isinstance(event.option, BookmarkOption)
        self.post_message(OpenLocation(event.option.bookmark.location))

    def check_action(self, action: str, parameters: tuple[object, ...]) -> bool | None:
        """Check if an action is possible to perform right now.

        Args:
            action: The action to perform.
            parameters: The parameters of the action.

        Returns:
            `True` if it can perform, `False` or `None` if not.
        """
        if not self.is_mounted:
            return False
        if action in ("rename", "delete"):
            return self.highlighted is not None
        return True

    @dataclass
    class BookmarksModified(Message):
        """A message indicating that the bookmarks have been modified."""

        bookmarks_viewer: BookmarksViewer
        """The new bookmarks."""

    @work
    async def action_rename(self) -> None:
        """Rename the currently-selected bookmark."""
        if self.highlighted is None:
            return
        bookmark_view = self.get_option_at_index(self.highlighted)
        assert isinstance(bookmark_view, BookmarkOption)
        if title := await self.app.push_screen_wait(
            ModalInput("Bookmark title", bookmark_view.bookmark.title)
        ):
            try:
                self.bookmarks[self.bookmarks.index(bookmark_view.bookmark)] = Bookmark(
                    title, bookmark_view.bookmark.location
                )
                with self.preserved_highlight:
                    self.mutate_reactive(BookmarksViewer.bookmarks)
                self.post_message(self.BookmarksModified(self))
            except ValueError:
                self.notify(
                    "Unable to find the bookmark to rename. It may have been removed.",
                    title="Error",
                    severity="error",
                )

    @work
    async def action_delete(self) -> None:
        """Delete the currently-selected bookmark."""
        if self.highlighted is None:
            return
        bookmark_view = self.get_option_at_index(self.highlighted)
        assert isinstance(bookmark_view, BookmarkOption)
        if await self.app.push_screen_wait(
            Confirm(
                "Delete bookmark",
                f"Are you sure you want to delete the bookmark '{escape(bookmark_view.bookmark.title)}'?",
            )
        ):
            try:
                del self.bookmarks[self.bookmarks.index(bookmark_view.bookmark)]
                with self.preserved_highlight:
                    self.mutate_reactive(BookmarksViewer.bookmarks)
                self.post_message(self.BookmarksModified(self))
            except ValueError:
                self.notify(
                    "Unable to find the bookmark to delete.",
                    title="Error",
                    severity="error",
                )


### bookmarks.py ends here
