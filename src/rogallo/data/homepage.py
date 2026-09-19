"""Provides code for saving and loading the home page."""

##############################################################################
# Python imports.
from functools import cache
from pathlib import Path
from typing import Final

##############################################################################
# Local imports.
from .locations import data_dir

##############################################################################
_DEFAULT_HOMEPAGE: Final[str] = "gemini://geminiprotocol.net/"
"""The default home page."""


##############################################################################
def homepage_file() -> Path:
    """Get the path for the home page file.

    Returns:
        The path for the home page file.
    """
    return data_dir() / "homepage"


##############################################################################
@cache
def load_homepage() -> str:
    """Load the home page from storage.

    Returns:
        The loaded home page.
    """
    return (
        homepage_file().read_text(encoding="utf-8").strip()
        if homepage_file().exists()
        else ""
    ) or _DEFAULT_HOMEPAGE


##############################################################################
def save_homepage(homepage: str) -> str:
    """Save the home page to storage.

    Args:
        homepage: The home page to save.

    Returns:
        The saved home page.
    """
    load_homepage.cache_clear()
    homepage_file().write_text(homepage.strip(), encoding="utf-8")
    return load_homepage()


### homepage.py ends here
