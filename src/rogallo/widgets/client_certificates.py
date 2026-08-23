"""Provides a client certificate manager widget for the application."""

##############################################################################
# Textual enhanced imports.
from textual_enhanced.widgets import EnhancedOptionList


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
    client certificates.
    """


### client_certificates.py ends here
