"""Provides the history panel widget."""

##############################################################################
# Textual imports.
from textual import on
from textual.reactive import var

##############################################################################
# Textual enhanced imports.
from textual_enhanced.widgets import EnhancedOptionList

##############################################################################
# Local imports.
from ..data import LocationHistory
from ..messages import OpenLocation


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
        self.clear_options().add_options(str(location) for location in self.history)
        self.highlighted = self.history.current_location

    def update_from_history(self) -> None:
        """Update the content of the history viewer."""
        self.mutate_reactive(HistoryViewer.history)

    @on(EnhancedOptionList.OptionSelected)
    def _jump_to_history(self, event: EnhancedOptionList.OptionSelected) -> None:
        """Jump to the selected history location."""
        event.stop()
        self.history.goto(event.option_index)
        if self.history.current_item is not None:
            self.post_message(
                OpenLocation(self.history.current_item, from_history=True)
            )


### history.py ends here
