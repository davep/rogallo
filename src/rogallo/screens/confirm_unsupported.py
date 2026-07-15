"""Provides a dialog for confirming the opening of an unsupported URI."""

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
type Confirmation = Literal["once", "always"] | None
"""Type of the data returned from the confirmation dialog."""


##############################################################################
class ConfirmUnsupportedURI(ModalScreen[Confirmation]):
    """A modal screen to confirm the opening of an unsupported URI."""

    CSS = """
    ConfirmUnsupportedURI {
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

    BINDINGS = [("o", "open_once"), ("a", "open_always"), ("escape", "cancel")]

    def __init__(self, uri: str, description: str) -> None:
        """Initialise the screen.

        Args:
            uri: The URI to confirm.
            description: A description for the confirmation.
        """
        super().__init__()
        self._uri = uri
        """The URI to confirm."""
        self._description = description
        """The description for the configuration dialog."""

    def compose(self) -> ComposeResult:
        """Compose the screen.

        Returns:
            The composed screen.
        """
        with VerticalGroup() as dialog:
            dialog.border_title = f"Open {self._uri}?"
            yield Label(self._description, shrink=True, markup=False)
            with HorizontalGroup(id="buttons"):
                yield Button(add_key("Once", "o"), id="once", variant="success")
                yield Button(add_key("Always", "a"), id="always", variant="success")
                yield Button(add_key("Cancel", "Esc"), id="cancel", variant="error")

    @on(Button.Pressed, "#once")
    def action_open_once(self) -> None:
        """Allow opening this once.

        Args:
            message: The button pressed message.
        """
        self.dismiss("once")

    @on(Button.Pressed, "#always")
    def action_open_always(self) -> None:
        """Allow always opening.

        Args:
            message: The button pressed message.
        """
        self.dismiss("always")

    @on(Button.Pressed, "#cancel")
    def action_cancel(self) -> None:
        """Cancel opening the URI."""
        self.dismiss(None)


### confirm_unsupported.py ends here
