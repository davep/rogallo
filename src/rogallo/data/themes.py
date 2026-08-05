"""Support for custom themes."""

##############################################################################
# Python imports.
from collections.abc import Iterator
from dataclasses import fields
from json import JSONDecodeError, loads
from pathlib import Path
from typing import Final

##############################################################################
# Textual imports.
from textual.theme import Theme

##############################################################################
# Local imports.
from .locations import config_dir


##############################################################################
def themes_dir() -> Path:
    """The path to the directory that holds the themes.

    Returns:
        The path to the directory that holds the themes.
    """
    return config_dir() / "themes"


##############################################################################
_WANTED: Final[set[str]] = {field.name for field in fields(Theme)}
"""The set of fields that are wanted from the theme files."""


##############################################################################
def load_themes() -> Iterator[Theme]:
    """Get the list of themes.

    Returns:
        The list of themes.
    """
    for theme in themes_dir().glob("*.json"):
        try:
            data = loads(theme.read_text(encoding="utf-8"))
        except JSONDecodeError:
            continue
        yield Theme(
            **{field: value for field, value in data.items() if field in _WANTED}
        )


### themes.py ends here
