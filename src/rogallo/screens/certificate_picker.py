"""Provides a dialog that lets a user pick a certificate from the local store."""

##############################################################################
# Python imports.
from collections.abc import Iterable
from typing import Literal

##############################################################################
# Textual imports.
from textual import on
from textual.app import ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup
from textual.getters import query_one
from textual.screen import ModalScreen
from textual.widgets import Button, Label, OptionList
from textual.widgets.option_list import Option

##############################################################################
# Textual enhanced imports.
from textual_enhanced.tools import add_key

##############################################################################
# Wasat imports.
from wasat import ClientCertificate, GeminiURI

##############################################################################
type ClientCertificatePickerResult = ClientCertificate | Literal["create"] | None


##############################################################################
class Certificate(Option):
    """An option that represents a client certificate."""

    def __init__(self, certificate: ClientCertificate) -> None:
        """Initialize the option.

        Args:
            certificate: The certificate to represent.
        """
        super().__init__(certificate.subject_common_name or "Unnamed")
        self._certificate = certificate
        """The certificate to represent."""

    @property
    def certificate(self) -> ClientCertificate:
        """The certificate represented by this option."""
        return self._certificate


##############################################################################
class ClientCertificatePicker(ModalScreen[ClientCertificatePickerResult]):
    """A dialog that lets a user pick a certificate from the local store."""

    DEFAULT_CSS = """
    ClientCertificatePicker {
        align: center middle;

        &> VerticalGroup {
            width: 50%;
            height: auto;
            background: $panel;
            border: panel $border;

            OptionList {
                height: auto;
                max-height: 20;
            }

            Label {
                padding: 0 1 1 1;
            }

            Button {
                margin-left: 1;
            }

            #buttons {
                margin: 1 1 0 1;
                align: right middle;
            }
        }
    }
    """

    BINDINGS = [
        ("escape", "cancel"),
        ("f2", "create"),
    ]

    _certificate_choices = query_one(OptionList)
    """The option list that contains the certificate choices."""

    def __init__(
        self, uri: GeminiURI, certificates: Iterable[ClientCertificate]
    ) -> None:
        """Initialize the dialog.

        Args:
            uri: The URI that is requesting a client certificate.
            certificates: The certificates to display in the dialog.
        """
        super().__init__()
        self._uri = uri
        """The URI that is requesting a client certificate."""
        self._certificates = sorted(
            certificates, key=lambda c: (c.subject_common_name or "Unnamed").casefold()
        )
        """The certificates to display in the dialog."""

    def compose(self) -> ComposeResult:
        """Compose the dialog."""
        with VerticalGroup() as dialog:
            dialog.border_title = "Client certificates"
            yield Label(
                f"The site [italic $accent]{self._uri}[/] is requesting a client certificate. "
                "You can pick an existing one or create a new one.",
                shrink=True,
            )
            yield OptionList(
                *(Certificate(certificate) for certificate in self._certificates)
            )
            with HorizontalGroup(id="buttons"):
                yield Button(add_key("Select", "Enter"), id="select", variant="success")
                yield Button(add_key("Create New", "F2"), id="create")
                yield Button(add_key("Cancel", "Esc"), id="cancel", variant="error")

    @on(OptionList.OptionSelected)
    @on(Button.Pressed, "#select")
    def action_select(self) -> None:
        """Select the currently highlighted certificate."""
        if self._certificate_choices.highlighted is not None:
            selected = self._certificate_choices.get_option_at_index(
                self._certificate_choices.highlighted
            )
            assert isinstance(selected, Certificate)
            self.dismiss(selected.certificate)

    @on(Button.Pressed, "#create")
    def action_create(self) -> None:
        """Create a new certificate."""
        self.dismiss("create")

    @on(Button.Pressed, "#cancel")
    def action_cancel(self) -> None:
        """Cancel the dialog."""
        self.dismiss(None)


### certificate_picker.py ends here
