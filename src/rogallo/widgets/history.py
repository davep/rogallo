"""Provides the history panel widget."""

##############################################################################
# Python imports.
from datetime import datetime
from pathlib import Path

##############################################################################
# Rich imports.
from rich.markup import escape

##############################################################################
# Textual imports.
from textual import on
from textual.reactive import var
from textual.widgets.option_list import Option

##############################################################################
# Textual enhanced imports.
from textual_enhanced.widgets import EnhancedOptionList

##############################################################################
# Wasat imports.
from wasat.uri import GEMINI_PREFIX, GeminiURI

##############################################################################
# Local imports.
from ..data import LocationHistory, LocationVisit
from ..messages import OpenLocation
from ..types import GeminiLocation


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

    def __init__(self, visit: LocationVisit) -> None:
        """Initialise the history option.

        Args:
            visit: The visit to display.
        """
        self._location = visit.location
        """The location to display."""
        super().__init__(
            (
                f"{escape(self._location_display)}\n"
                f"[dim i]{_clean_time(visit.timestamp)}[/]"
            ),
            id=str(visit.location),
        )

    @property
    def _location_display(self) -> str:
        """Get the display string for the location.

        Returns:
            The display string for the location.
        """
        if isinstance(self._location, GeminiURI):
            return str(self._location).removeprefix(GEMINI_PREFIX)
        try:
            return (Path("~") / self._location.relative_to(Path.home())).as_posix()
        except ValueError:
            return self._location.as_posix()

    @property
    def location(self) -> GeminiLocation:
        """The location for this option."""
        return self._location


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

    HELP = """
    ## Location history

    This is your locations history. Here you can revisit locations you've
    viewed, and also remove individual or all locations.
    """

    history: var[LocationHistory] = var(LocationHistory())
    """The history of visited locations."""

    def _watch_history(self) -> None:
        """Update the history viewer when the history changes."""
        self.clear_options().add_options(
            HistoryOption(visit) for visit in reversed(list(self.history))
        )
        if self.option_count:
            self.highlighted = 0

    @on(EnhancedOptionList.OptionSelected)
    def _jump_to_history(self, event: EnhancedOptionList.OptionSelected) -> None:
        """Jump to the selected history location."""
        event.stop()
        assert isinstance(event.option, HistoryOption)
        self.post_message(OpenLocation(event.option.location))


### history.py ends here
