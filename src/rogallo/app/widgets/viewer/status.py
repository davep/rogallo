"""Provides the status bar widget for the viewer."""

##############################################################################
# Textual imports.
from textual.reactive import var
from textual.widgets import Label


##############################################################################
class ViewerStatus(Label):
    """A widget for displaying the status of the viewer."""

    DEFAULT_CSS = """
    ViewerStatus {
        background: $panel;
        color: $text-muted;
        width: 1fr;
        height: 1;
        padding: 0 1;
    }
    """

    message: var[str] = var("", always_update=True)
    """The message to display in the status bar."""

    def _watch_message(self) -> None:
        """React to the message changing."""
        if (
            len(
                display := ""
                if self.message is None
                else str(self.message)[-self.size.width :]
            )
            >= self.size.width
        ):
            display = f"…{display[1:]}"
        self.update(display)

    def on_resize(self) -> None:
        """Handle the widget being resized."""
        self.message = self.message


### status.py ends here
