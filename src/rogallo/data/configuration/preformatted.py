"""Provides code for loading the preformatted configuration."""

##############################################################################
# Python imports.
from dataclasses import dataclass, field
from functools import cache
from typing import TypedDict

##############################################################################
# Local imports.
from ._loader import load_configuration_into


##############################################################################
class Hide(TypedDict):
    """Specification for a instance of pre-formatted text to hide."""

    uri_prefix: str
    """The URI prefix of the page to hide on."""
    alt_text: str
    """The alt text of the pre-formatted text to hide."""


##############################################################################
@dataclass(frozen=True)
class PreformattedConfiguration:
    """Preformatted configuration data."""

    blend_with_background: list[str] = field(default_factory=lambda: [""])
    """List of types of pre-formatted text to blend with the background."""

    hide: list[Hide] = field(default_factory=list)
    """List of pre-formatted text to hide."""

    tooltips: bool = True
    """Should tooltips be shown for preformatted text?"""


##############################################################################
@cache
def load_preformatted() -> PreformattedConfiguration:
    """Load the preformatted configuration.

    Returns:
        The loaded preformatted configuration.
    """
    return load_configuration_into(PreformattedConfiguration, "preformatted")


### preformatted.py ends here
