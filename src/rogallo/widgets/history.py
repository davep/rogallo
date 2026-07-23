"""Provides the history panel widget."""

##############################################################################
# Python future imports.
from __future__ import annotations

##############################################################################
# Python imports.
from dataclasses import dataclass
from datetime import datetime

##############################################################################
# Textual imports.
from textual import on, work
from textual.message import Message
from textual.reactive import var
from textual.widgets.option_list import Option

##############################################################################
# Textual enhanced imports.
from textual_enhanced.binding import HelpfulBinding
from textual_enhanced.dialogs import Confirm
from textual_enhanced.widgets import EnhancedOptionList

##############################################################################
# Local imports.
from ..data import LocationHistory, LocationVisit
from ..messages import OpenLocation
from ..safe_escape import escape
from ..types import RogalloLocation, short_location


##############################################################################
def _clean_time(timestamp: datetime) -> datetime:
    """Clean a timestamp for display.

    Args:
        timestamp: The timestamp to clean.

    Returns:
        The cleaned timestamp.
    """
    return timestamp.replace(microsecond=0)


##############################################################################
class HistoryOption(Option):
    """An option for the history viewer."""

    def __init__(self, visit: LocationVisit, history_position: int) -> None:
        """Initialise the history option.

        Args:
            visit: The visit to display.
            history_position: The position of the visit in the history.
        """
        self._location = visit.location
        """The location to display."""
        super().__init__(
            (
                f"{escape(short_location(visit.location))}\n"
                f"[dim i]{_clean_time(visit.timestamp)}[/]"
            ),
            id=str(visit.location),
        )
        self._history_position = history_position
        """The position of the visit in the history."""

    @property
    def location(self) -> RogalloLocation:
        """The location for this option."""
        return self._location

    @property
    def history_position(self) -> int:
        """The position of the visit in the history."""
        return self._history_position


##############################################################################
class HistoryViewer(EnhancedOptionList):
    """A widget for displaying the history of visited locations."""

    DEFAULT_CSS = """
    HistoryViewer {
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

    DEFAULT_CLASSES = "panel"

    HELP = """
    ## Location history

    This is your locations history. Here you can revisit locations you've
    viewed, and also remove individual or all locations.
    """

    BINDINGS = [
        HelpfulBinding(
            "d",
            "delete_location",
            "Delete",
            show=True,
            tooltip="Delete the selected location from the history",
        ),
        HelpfulBinding(
            "D",
            "delete_all_locations",
            "Clear",
            show=True,
            tooltip="Delete all locations from the history",
        ),
    ]

    history: var[LocationHistory] = var(LocationHistory())
    """The history of visited locations."""

    def _watch_history(self) -> None:
        """Update the history viewer when the history changes."""
        self.clear_options().add_options(
            HistoryOption(visit, position)
            for position, visit in reversed(list(enumerate(self.history)))
        )
        if self.option_count:
            self.highlighted = 0

    @on(EnhancedOptionList.OptionSelected)
    def _jump_to_history(self, event: EnhancedOptionList.OptionSelected) -> None:
        """Jump to the selected history location."""
        event.stop()
        assert isinstance(event.option, HistoryOption)
        self.post_message(OpenLocation(event.option.location))

    @dataclass
    class HistoryModified(Message):
        """A message sent when the history is modified."""

        history_viewer: HistoryViewer
        """The history viewer that was modified."""

    @work
    async def action_delete_location(self) -> None:
        """Delete the selected location from the history."""
        if self.highlighted is not None and await self.app.push_screen_wait(
            Confirm("Delete location", "Are you sure you want to delete this location?")
        ):
            assert isinstance(
                location := self.get_option_at_index(self.highlighted), HistoryOption
            )
            del self.history[location.history_position]
            with self.preserved_highlight:
                self.mutate_reactive(HistoryViewer.history)
            self.post_message(self.HistoryModified(self))
            self.notify(f"{location.location} deleted", title="Location history")

    @work
    async def action_delete_all_locations(self) -> None:
        """Delete all locations from the history."""
        if self.option_count > 0 and await self.app.push_screen_wait(
            Confirm(
                "Delete all locations", "Are you sure you want to delete all locations?"
            )
        ):
            self.history.clear()
            self.mutate_reactive(HistoryViewer.history)
            self.post_message(self.HistoryModified(self))
            self.notify("All locations deleted", title="Location history")


### history.py ends here
