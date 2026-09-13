"""Provides code for loading the command line aliases."""

##############################################################################
# Python imports.
from functools import cache
from typing import Final

##############################################################################
# Local imports.
from ._loader import load_configuration

##############################################################################
type Aliases = dict[str, str]
"""Type for aliases."""

##############################################################################
_DEFAULT_ALIASES: Final[Aliases] = {
    "fg": "gopher://gopher.floodgap.com/1/v2/vs?{q}",
    "gp": "gemini://gemi.dev/cgi-bin/wp.cgi/search?{q}",
    "ken": "gemini://kennedy.gemi.dev/search?{q}",
    "tlgs": "gemini://tlgs.one/search?{q}",
}
"""The default aliases."""


##############################################################################
@cache
def load_aliases() -> Aliases:
    """Load the aliases.

    Returns:
        The loaded aliases.
    """
    return load_configuration("aliases", _DEFAULT_ALIASES)


### aliases.py ends here
