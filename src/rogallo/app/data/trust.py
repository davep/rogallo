"""Functions for getting the path to the trust file."""

##############################################################################
# Python imports.
from pathlib import Path

##############################################################################
# Local imports.
from .locations import data_dir


##############################################################################
def trust_file() -> Path:
    """The path to the directory that holds the trust file.

    Returns:
        The path to the directory that holds the trust file.
    """
    return data_dir() / "known_hosts"


### trust.py ends here
