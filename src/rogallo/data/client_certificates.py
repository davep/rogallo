"""Functions for getting the path to the client certificates directory."""

##############################################################################
# Python imports.
from pathlib import Path

##############################################################################
# Local imports.
from .locations import data_dir


##############################################################################
def client_certificates_directory() -> Path:
    """The path to the directory that holds the client certificates.

    Returns:
        The path to the directory that holds the client certificates.
    """
    return data_dir() / "client_certificates"


### client_certificates.py ends here
