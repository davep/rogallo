"""Provides a security alert screen for the Rogallo application."""

##############################################################################
# Python imports.
from typing import Literal

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
type SecurityAlertResult = Literal["forget", "ignore", "cancel"]
"""Possible result values for the security alert screen."""


##############################################################################
class SecurityAlert(ModalScreen[SecurityAlertResult]):
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

        #message {
            width: 100%;
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
        ("i", "ignore"),
        ("escape", "cancel"),
        ("left, up", "app.focus_previous"),
        ("right, down", "app.focus_next"),
    ]

    def __init__(self, uri: RogalloLocation, message: str, can_ignore: bool) -> None:
        """Initialise the screen.

        Args:
            uri: The location of the security alert.
            message: The security alert message.
            can_ignore: Whether the user can ignore the security alert.
        """
        super().__init__()
        self._uri = uri
        """The location of the security alert."""
        self._message = message
        """The security alert message."""
        self._can_ignore = can_ignore
        """Whether the user can ignore the security alert."""

    def compose(self) -> ComposeResult:
        """Compose the screen.

        Yields:
            The widgets for the screen.
        """
        preamble = (
            "You can choose to forget the certificate and try again, ignore the security alert and continue, or cancel the connection."
            if self._can_ignore
            else "You can choose to forget the certificate and try again, or cancel the connection."
        )
        with VerticalGroup() as dialog:
            dialog.border_title = "Security error!"
            yield Label(f"Security alert for {self._uri}", shrink=True, markup=False)
            yield Label(self._message, shrink=True, variant="error", id="message")
            yield Label(
                f"{preamble} NOTE: There are a number of reasons why you might be seeing this error. "
                "If you are unsure, it is recommended to cancel the connection and investigate further.",
                shrink=True,
            )
            with HorizontalGroup(id="buttons"):
                yield Button(add_key("Cancel", "Esc"), id="cancel", variant="primary")
                yield Button(add_key("Forget", "f"), id="forget", variant="error")
                if self._can_ignore:
                    yield Button(add_key("Ignore", "i"), id="ignore", variant="warning")

    @on(Button.Pressed, "#cancel")
    def action_cancel(self) -> None:
        """Cancel the security alert."""
        self.dismiss("cancel")

    @on(Button.Pressed, "#forget")
    def action_forget(self) -> None:
        """Forget the certificate and try again."""
        self.dismiss("forget")

    @on(Button.Pressed, "#ignore")
    def action_ignore(self) -> None:
        """Ignore the security alert and continue."""
        self.dismiss("ignore")


### security_alert.py ends here
