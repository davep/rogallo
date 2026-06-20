"""Provides the title widget for the viewer."""

##############################################################################
# Textual imports.
from textual.reactive import var
from textual.widgets import Label

##############################################################################
# Local imports.
from ...types import GeminiLocation


##############################################################################
class ViewerTitle(Label):
    """A widget for displaying the title of the viewer."""

    DEFAULT_CSS = """
    ViewerTitle {
        background: $panel;
        color: $foreground;
        content-align: right middle;
        width: 1fr;
        height: 1;
    }
    """

    location: var[GeminiLocation | None] = var(None, always_update=True)
    """The location to display."""

    def _watch_location(self) -> None:
        """React to the location changing."""
        if (
            len(
                display := ""
                if self.location is None
                else str(self.location)[-self.size.width :]
            )
            >= self.size.width
        ):
            display = f"…{display[1:]}"
        self.update(display)

    def on_resize(self) -> None:
        """Handle the widget being resized."""
        self.location = self.location


### title.py ends here
