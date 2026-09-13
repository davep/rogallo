"""Provides code for loading keyboard bindings."""

##############################################################################
# Python imports.
from pathlib import Path

##############################################################################
# Textual imports.
from textual.binding import Keymap

##############################################################################
# PyYAML imports.
from yaml import YAMLError, safe_load

##############################################################################
# Local imports.
from ..locations import config_dir


##############################################################################
def bindings_file() -> Path:
    """The path to the file that holds the keyboard bindings.

    Returns:
        The path to the bindings file.
    """
    return config_dir() / "bindings.yaml"


##############################################################################
def load_bindings() -> Keymap:
    """Load the keyboard bindings.

    Returns:
        The loaded keyboard bindings.
    """
    try:
        return safe_load(bindings_file().read_text(encoding="utf-8")) or {}
    except (OSError, YAMLError):
        return {}


### bindings.py ends here
