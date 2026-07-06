"""Provides the status bar widget for the viewer."""

##############################################################################
# Textual imports.
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.getters import query_one
from textual.reactive import var
from textual.widgets import Label

##############################################################################
# Local imports.
from ...types import is_gemini_mime_type


##############################################################################
class ViewerStatus(Horizontal):
    """A widget for displaying the status of the viewer."""

    DEFAULT_CSS = """
    ViewerStatus {
        background: $panel;
        color: $text-muted;
        width: 1fr;
        height: 1;
        padding: 0 1;

        #message {
            width: 1fr;
        }
        #mime-type {
            width: auto;
            &.--gemini {
                 color: $text-success;
            }
        }
    }
    """

    message: var[str] = var("", always_update=True)
    """The message to display in the status bar."""
    mime_type: var[str] = var("", always_update=True)
    """The MIME type to display in the status bar."""

    _message = query_one("#message", Label)
    """The label for the message."""
    _mime_type = query_one("#mime-type", Label)
    """The label for the MIME type."""

    def compose(self) -> ComposeResult:
        """Compose the child widgets."""
        yield Label(id="message")
        yield Label(id="mime-type")

    def _watch_message(self) -> None:
        """React to the message changing."""
        if (
            len(
                display := ""
                if self.message is None
                else str(self.message)[-self._message.size.width :]
            )
            >= self._message.size.width
        ):
            display = f"…{display[1:]}"
        self._message.update(display)

    def _watch_mime_type(self) -> None:
        """React to the MIME type changing."""
        self._mime_type.update(self.mime_type)
        self._mime_type.set_class(is_gemini_mime_type(self.mime_type), "--gemini")

    def on_resize(self) -> None:
        """Handle the widget being resized."""
        self.message = self.message


### status.py ends here
