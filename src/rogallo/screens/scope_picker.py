"""Provides a modal dialog for picking a scope from a client certificate."""

##############################################################################
# Textual imports.
from textual import on
from textual.app import ComposeResult
from textual.containers import VerticalGroup
from textual.screen import ModalScreen
from textual.widgets import OptionList
from textual.widgets.option_list import Option

##############################################################################
# Wasat imports.
from wasat import ClientCertificate


##############################################################################
class Scope(Option):
    """An option for a scope."""

    def __init__(self, scope: str) -> None:
        """Initialise the option."""
        super().__init__(scope)
        self._scope = scope
        """The scope."""

    @property
    def scope(self) -> str:
        """Return the scope."""
        return self._scope


##############################################################################
class ScopePicker(ModalScreen[str | None]):
    """A modal screen to pick a scope from a client certificate."""

    CSS = """
    ScopePicker {
        align: center middle;
        &> VerticalGroup {
            background: $panel;
            border: panel $border;
            width: auto;
            height: auto;
            max-height: 80%;
            max-width: 80%;
            padding-top: 1;
        }
        OptionList {
            &, &:focus {
                border: none;
                background: $panel;
                background-tint: $panel 0%;
            }
            width: auto;
            min-width: 30;
            height: auto;
        }
    }
    """

    BINDINGS = [
        ("escape", "cancel", "Cancel"),
    ]

    def __init__(self, certificate: ClientCertificate, caption: str) -> None:
        """Initialise the screen."""
        super().__init__()
        self._certificate = certificate
        """The client certificate to pick a scope from."""
        self._caption = caption
        """The caption to show above the select widget."""

    def compose(self) -> ComposeResult:
        """Compose the screen."""
        with VerticalGroup() as dialog:
            dialog.border_title = self._caption
            yield OptionList(*(Scope(scope) for scope in self._certificate.scopes))

    @on(OptionList.OptionSelected)
    def action_select(self, event: OptionList.OptionSelected) -> None:
        """Select the scope."""
        assert isinstance(event.option, Scope)
        self.dismiss(event.option.scope)

    def action_cancel(self) -> None:
        """Cancel the selection."""
        self.dismiss(None)


### scope_picker.py ends here
