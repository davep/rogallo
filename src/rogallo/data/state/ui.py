"""Provides code for saving and loading UI state."""

##############################################################################
# Python imports.
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import asdict, dataclass, fields
from functools import cache
from json import dumps, loads
from pathlib import Path
from typing import Final

##############################################################################
# Local imports.
from ..locations import state_dir


##############################################################################
@dataclass
class UIState:
    """The state of the UI."""

    theme: str | None = None
    """The theme for the application."""

    side_panel_visible: bool = False
    """Should the sidepanel be visible?"""

    side_panel_on_right: bool = False
    """Should the sidepanel be on the right?"""

    side_panel_chosen_tab: str = "bookmarks"
    """The tab that should be chosen in the sidepanel."""

    strip_emoji: bool = False
    """Should emoji be stripped from text content?"""

    stripe_links: bool = False
    """Should links be given alternating backgrounds to help them stand out?"""

    with_link_jumps: bool = True
    """Should the application support jumping to links via numeric labels?"""

    cosy_link_jumps: bool = False
    """Should the numeric labels be displayed in a cosy way?"""

    handle_ansi_escape_sequences: bool = True
    """Should ANSI escape sequences be handled in text content?"""


##############################################################################
def ui_state_file() -> Path:
    """The path to the file that holds UI state information.

    Returns:
        The path to the UI state information file.
    """
    return state_dir() / "ui.json"


##############################################################################
_WANTED: Final[set[str]] = {field.name for field in fields(UIState)}
"""The set of fields that are wanted from the UI state file."""


##############################################################################
@cache
def load_ui_state() -> UIState:
    """Load the UI state from storage.

    Returns:
        The loaded UI state.
    """
    return UIState(
        **{
            field: value
            for field, value in loads(source.read_text(encoding="utf-8")).items()
            if field in _WANTED
        }
        if (source := ui_state_file()).exists()
        else {}
    )


##############################################################################
def save_ui_state(ui_state: UIState) -> UIState:
    """Save the UI state to storage.

    Args:
        ui_state: The UI state to save.

    Returns:
        The saved UI state.
    """
    load_ui_state.cache_clear()
    ui_state_file().write_text(
        dumps(asdict(ui_state), indent=4),
        encoding="utf-8",
    )
    return load_ui_state()


##############################################################################
@contextmanager
def update_ui_state() -> Iterator[UIState]:
    """Update the UI state in storage.

    Yields:
        The current UI state.
    """
    current_state = load_ui_state()
    try:
        yield current_state
    finally:
        save_ui_state(current_state)


### ui.py ends here
