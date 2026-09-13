"""Provides code for loading the command line aliases."""

##############################################################################
# Python imports.
from functools import cache
from pathlib import Path
from typing import Final

##############################################################################
# PyYAML imports.
from yaml import YAMLError, safe_dump, safe_load

##############################################################################
# Local imports.
from ..locations import config_dir

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
def aliases_file() -> Path:
    """The path to the file that holds the aliases.

    Returns:
        The path to the aliases file.
    """
    return config_dir() / "aliases.yaml"


##############################################################################
@cache
def load_aliases() -> Aliases:
    """Load the aliases.

    Returns:
        The loaded aliases.
    """
    if not aliases_file().exists():
        aliases_file().write_text(safe_dump(_DEFAULT_ALIASES), encoding="utf-8")
    try:
        return safe_load(aliases_file().read_text(encoding="utf-8")) or {}
    except (OSError, YAMLError):
        return {}


### aliases.py ends here
