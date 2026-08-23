"""Provides a client certificate manager widget for the application."""

##############################################################################
# Textual imports.
from textual.widgets.option_list import Option

##############################################################################
# Textual enhanced imports.
from textual_enhanced.widgets import EnhancedOptionList

##############################################################################
# Wasat imports.
from wasat import Client, ClientCertificate

##############################################################################
# Local imports.
from ..safe_escape import escape


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
        scoptes = "\n".join(f"[dim]{scope}[/]" for scope in certificate.scopes)
        super().__init__(
            (f"{escape(certificate.issuer_common_name or 'Unknown')}\n" f"{scoptes}")
        )


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
                    for certificate in await self._client.client_cert_store.list_certificates()
                ]
            )


### client_certificates.py ends here
