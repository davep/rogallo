"""Provides support for editing with an external editor."""

##############################################################################
# Python imports.
from functools import cache
from os import getenv
from pathlib import Path
from subprocess import run
from tempfile import NamedTemporaryFile
from typing import Any

##############################################################################
# Textual imports.
from textual.app import App

##############################################################################
# Local imports.
from .data import load_configuration
from .types import DEFAULT_GEMINI_EXTENSION


##############################################################################
@cache
def external_editor() -> str | None:
    """The external editor to use, if any."""
    return (
        load_configuration().external_editor
        or getenv("VISUAL")
        or getenv("EDITOR")
        or None
    )


##############################################################################
def edit_externally(application: App[Any], text: str) -> str:
    """Edit the given text in an external editor.

    Args:
        text: The text to edit.

    Returns:
        The edited text, or the original text if no external editor is
        configured.
    """
    if not (editor := external_editor()):
        return text
    with NamedTemporaryFile(
        mode="w+", delete=False, encoding="utf-8", suffix=DEFAULT_GEMINI_EXTENSION
    ) as temp_file:
        user_input = Path(temp_file.name)
        temp_file.write(text)
        temp_file.close()
        try:
            with application.suspend():
                run((editor, user_input))
                return user_input.read_text(encoding="utf-8")
        finally:
            user_input.unlink(missing_ok=True)


### editor.py ends here
