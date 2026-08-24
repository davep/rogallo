"""Provides a client certificate manager widget for the application."""

##############################################################################
# Textual imports.
from textual import work
from textual.widgets.option_list import Option

##############################################################################
# Textual enhanced imports.
from textual_enhanced.binding import HelpfulBinding
from textual_enhanced.dialogs import Confirm
from textual_enhanced.widgets import EnhancedOptionList

##############################################################################
# Wasat imports.
from wasat import Client, ClientCertificate

##############################################################################
# Local imports.
from ..safe_escape import escape


##############################################################################
def _name(certificate: ClientCertificate) -> str:
    """Return the name of the certificate.

    Args:
        certificate: The certificate to get the name of.

    Returns:
        The name of the certificate.
    """
    return certificate.issuer_common_name or "Unnamed"


##############################################################################
class CertificateOption(Option):
    """An option for the client certificate manager."""

    def __init__(self, certificate: ClientCertificate) -> None:
        """Initialise the certificate option.

        Args:
            certificate: The certificate to display.
        """
        self._certificate = certificate
        """The certificate to display."""
        scopes = "\n".join(f"[dim]{scope}[/]" for scope in certificate.scopes)
        super().__init__(
            f"{escape(_name(certificate))}\n"
            f"{scopes}\n"
            f"[dim][bold]Expires[/bold]: {certificate.not_after}[/]"
        )

    @property
    def certificate(self) -> ClientCertificate:
        """The certificate for this option."""
        return self._certificate


##############################################################################
class ClientCertificateManager(EnhancedOptionList):
    """A widget that manages client certificates for the application."""

    DEFAULT_CSS = """
    ClientCertificateManager {
        height: 1fr;
        border: none;
        text-wrap: nowrap;
        text-overflow: ellipsis;
        &:focus {
            border: none;
            background: $panel;
        }
    }
    """

    DEFAULT_CLASSES = "panel"

    HELP = """
    ## Client certificates

    These are your client certificates. Here you can view, add, and remove
    them.
    """

    BINDINGS = [
        HelpfulBinding(
            "d", "delete", "Delete", tooltip="Delete the selected certificate"
        ),
    ]

    def __init__(self, client: Client) -> None:
        """Initialize the client certificate manager widget."""
        super().__init__()
        self._client = client
        """The client for which to manage certificates."""

    def on_mount(self) -> None:
        """Called when the widget is mounted."""
        self.call_next(self._load_certificates)

    async def _load_certificates(self) -> None:
        """Load the client certificates into the widget."""
        with self.preserved_highlight:
            self.clear_options().add_options(
                [
                    CertificateOption(certificate)
                    for certificate in sorted(
                        await self._client.client_cert_store.list_certificates(),
                        key=lambda certificate: _name(certificate).casefold(),
                    )
                ]
            )

    @work
    async def action_delete(self) -> None:
        """Delete the selected certificate."""
        if (
            self.highlighted is not None
            and isinstance(option := self.options[self.highlighted], CertificateOption)
            and await self.app.push_screen_wait(
                Confirm(
                    "Delete certificate?",
                    f"Are you sure you want to delete '{_name(option.certificate)}'?",
                )
            )
        ):
            await self._client.client_cert_store.delete_certificate(option.certificate)
            await self._load_certificates()
            self.notify(escape(_name(option.certificate)), title="Deleted")


### client_certificates.py ends here
