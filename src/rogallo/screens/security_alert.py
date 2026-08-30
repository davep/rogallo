"""Provides a security alert screen for the Rogallo application."""

##############################################################################
# Textual imports.
from textual import on
from textual.app import ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup
from textual.screen import ModalScreen
from textual.widgets import Button, Label

##############################################################################
# Textual enhanced imports.
from textual_enhanced.tools import add_key

##############################################################################
# Local imports.
from ..types import RogalloLocation


##############################################################################
class SecurityAlert(ModalScreen[bool]):
    """A modal screen to display a security alert."""

    CSS = """
    SecurityAlert {
        align: center middle;

        &> VerticalGroup {
            width: 60%;
            height: auto;
            background: $panel;
            border: panel $border;
        }

        Label {
            padding: 1 2;
            height: auto;
        }

        Button {
            margin-right: 1;
        }

        #buttons {
            height: auto;
            margin-top: 1;
            align-horizontal: right;
        }
    }
    """

    BINDINGS = [
        ("f", "forget"),
        ("escape", "cancel"),
        ("left, up", "app.focus_previous"),
        ("right, down", "app.focus_next"),
    ]

    def __init__(self, uri: RogalloLocation, message: str) -> None:
        """Initialise the screen.

        Args:
            location (RogalloLocation): The location of the security alert.
            message (str): The security alert message.
        """
        super().__init__()
        self._uri = uri
        """The location of the security alert."""
        self._message = message
        """The security alert message."""

    def compose(self) -> ComposeResult:
        """Compose the screen.

        Returns:
            The composed screen.
        """
        with VerticalGroup() as dialog:
            dialog.border_title = "Security error!"
            yield Label(f"Security alert for {self._uri}", shrink=True, markup=False)
            yield Label(self._message, shrink=True, variant="error")
            yield Label(
                "You can choose to forget the certificate and try again, or cancel the connection. "
                "NOTE: There are a number of reasons why you might be seeing this error. "
                "If you are unsure, it is recommended to cancel the connection and investigate further.",
                shrink=True,
            )
            with HorizontalGroup(id="buttons"):
                yield Button(add_key("Cancel", "Esc"), id="cancel", variant="primary")
                yield Button(add_key("Forget", "f"), id="forget", variant="error")

    @on(Button.Pressed, "#cancel")
    def action_cancel(self) -> None:
        """Cancel the security alert."""
        self.dismiss(False)

    @on(Button.Pressed, "#forget")
    def action_forget(self) -> None:
        """Forget the certificate and try again."""
        self.dismiss(True)


### security_alert.py ends here
