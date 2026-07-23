"""Provides the title widget for the viewer."""

##############################################################################
# Textual imports.
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.getters import query_one
from textual.reactive import var
from textual.widgets import Label

##############################################################################
# Local imports.
from ...types import RogalloLocation


##############################################################################
class ViewerTitle(Horizontal):
    """A widget for displaying the title of the viewer."""

    DEFAULT_CSS = """
    ViewerTitle {
        background: $panel;
        color: $foreground;
        height: 1;
        padding: 0 1;

        #lock-icon {
            width: 1;
            color: $text-success;
        }

        #location {
            width: 1fr;
            content-align: right middle;
        }
    }
    """

    location: var[RogalloLocation | None] = var(None, always_update=True)
    """The location to display."""
    needed_certificate: var[bool] = var(False)
    """Whether the location needed a certificate."""

    _lock_icon = query_one("#lock-icon", Label)
    """The label for the lock icon."""
    _location_label = query_one("#location", Label)
    """The label for the location."""

    def compose(self) -> ComposeResult:
        """Compose the child widgets."""
        yield Label(id="lock-icon")
        yield Label(id="location")

    def _watch_location(self) -> None:
        """React to the location changing."""
        if (
            len(
                display := ""
                if self.location is None
                else str(self.location)[-self._location_label.size.width :]
            )
            >= self._location_label.size.width
        ):
            display = f"…{display[1:]}"
        self._location_label.update(display)

    def _watch_needed_certificate(self) -> None:
        """React to the needed_certificate changing."""
        self._lock_icon.update("\u26bf" if self.needed_certificate else " ")

    def on_resize(self) -> None:
        """Handle the widget being resized."""
        self.location = self.location


### title.py ends here
