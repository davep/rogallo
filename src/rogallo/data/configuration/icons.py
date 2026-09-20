"""Provides code for loading icon configuration."""

##############################################################################
# Python imports.
from functools import cache
from typing import Final, TypedDict

##############################################################################
# PyYAML imports.
##############################################################################
# Local imports.
from ._io import load_configuration


##############################################################################
class Icons(TypedDict):
    """The icons configuration data."""

    geminispace_link: str
    """The icon to use for links to gemini:// URIs."""
    fingerspace_link: str
    """The icon to use for links to finger:// URIs."""
    gopherspace_link: str
    """The icon to use for links to gopher:// URIs."""
    spartanspace_link: str
    """The icon to use for links to spartan:// URIs."""
    nexspace_link: str
    """The icon to use for links to nex:// URIs."""
    titanspace_link: str
    """The icon to use for links to titan:// URIs."""
    otherspace_link: str
    """The icon to use for non-gemini URIs."""
    list_item_bullet: str
    """The icon to use for list item bullets."""
    client_certificate_used: str
    """The icon to use for indicating that a client certificate was used."""
    verified_ca: str
    """The icon to use for indicating that a server was verified by a CA."""
    verified_tofu: str
    """The icon to use for indicating that a server was verified by TOFU."""
    verified_off: str
    """The icon to use for indicating that server was off."""
    unverified: str
    """The icon to use for indicating that a server was not verified."""


##############################################################################
_DEFAULT_ICONS: Final[Icons] = {
    "geminispace_link": "⪢",
    "fingerspace_link": "☛",
    "gopherspace_link": "○",
    "spartanspace_link": "⪧",
    "nexspace_link": "☽",
    "titanspace_link": "⩓",
    "otherspace_link": "↗",
    "list_item_bullet": "•",
    "client_certificate_used": "⚿",
    "verified_ca": "⛉",
    "verified_tofu": "✓",
    "verified_off": "✗",
    "unverified": "•",
}


##############################################################################
@cache
def load_icons() -> Icons:
    """Load the icons configuration.

    Returns:
        The icons configuration.
    """
    return load_configuration("icons", _DEFAULT_ICONS)


### icons.py ends here
