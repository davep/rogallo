"""Provides the history panel widget."""

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
from wasat.uri import GEMINI_PREFIX

##############################################################################
# Local imports.
from ..data import LocationHistory
from ..messages import OpenLocation
from ..types import GeminiLocation


##############################################################################
class HistoryOption(Option):
    """An option for the history viewer."""

    def __init__(self, location: GeminiLocation) -> None:
        """Initialize the history option.

        Args:
            location: The location to display.
        """
        self._location = location
        """The location to display."""
        super().__init__(str(location).removeprefix(GEMINI_PREFIX), id=str(location))

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
        }
    }
    """

    history: var[LocationHistory] = var(LocationHistory())
    """The history of visited locations."""

    def _watch_history(self) -> None:
        """Update the history viewer when the history changes."""
        self.clear_options().add_options(
            HistoryOption(location) for location in reversed(list(self.history))
        )
        if self.option_count:
            self.highlighted = 0

    @on(EnhancedOptionList.OptionSelected)
    def _jump_to_history(self, event: EnhancedOptionList.OptionSelected) -> None:
        """Jump to the selected history location."""
        event.stop()
        assert isinstance(event.option, HistoryOption)
        self.post_message(OpenLocation(event.option.location, from_history=True))


### history.py ends here
