"""Provides a dialog for viewing the details of a certificate."""

##############################################################################
# Textual imports.
from textual import on
from textual.app import ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup
from textual.screen import ModalScreen
from textual.widgets import Button

##############################################################################
# Textual enhanced imports.
from textual_enhanced.tools import add_key

##############################################################################
# Wasat imports.
from wasat import ClientCertificate

##############################################################################
# Local imports.
from .data import Data


##############################################################################
class CertificateViewer(ModalScreen[None]):
    """A modal screen to show information about a certificate."""

    CSS = """
    CertificateViewer {
        align: center middle;

        &> VerticalGroup {
            height: auto;
            width: auto;
            max-width: 90%;
            max-height: 90%;
            background: $panel;
            border: panel $border;
        }

        #content {
            width: auto;
            height: auto;
            padding: 1 2;
            background: $surface;
        }

        #buttons {
            align: center middle;
            width: 100%;
            height: auto;
            padding-top: 1;
        }
    }
    """

    BINDINGS = [("escape", "close")]

    def __init__(self, certificate: ClientCertificate) -> None:
        """Initialise the screen.

        Args:
            certificate: The certificate to show information about.
        """
        super().__init__()
        self._certificate = certificate
        """The certificate to show information about."""

    def compose(self) -> ComposeResult:
        """Compose the screen."""
        with VerticalGroup() as dialog:
            dialog.border_title = "Certificate Details"
            with VerticalGroup(id="content"):
                yield Data(
                    "Subject Common Name",
                    self._certificate.subject_common_name or "N/A",
                )
                yield Data(
                    "Issuer Common Name", self._certificate.issuer_common_name or "N/A"
                )
                yield from Data.maybe("Email", self._certificate.email)
                yield from Data.maybe("User ID", self._certificate.user_id)
                yield from Data.maybe("Organisation", self._certificate.organisation)
                yield from Data.maybe("Country", self._certificate.country)
                yield Data("Not Before", str(self._certificate.not_before))
                yield Data("Not After", str(self._certificate.not_after))
                yield Data("Self-Signed", self._certificate.is_self_signed)
                yield Data("Serial Number", str(self._certificate.serial_number))
                yield Data("Fingerprint", self._certificate.fingerprint)
                yield Data("Key Type", self._certificate.key_type)
                yield Data("Key Size", str(self._certificate.key_size))
            with HorizontalGroup(id="buttons"):
                yield Button(add_key("Close", "Esc"), variant="primary", id="close")

    @on(Button.Pressed, "#close")
    def action_close(self) -> None:
        """Close the screen."""
        self.dismiss()


### certificate_viewer.py ends here
