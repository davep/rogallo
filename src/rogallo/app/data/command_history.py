"""Provides code for saving and loading the command history."""

##############################################################################
# Python imports.
from json import dumps, loads
from pathlib import Path

##############################################################################
# Local imports.
from ...history import RecencyHistory
from .locations import data_dir


##############################################################################
class CommandLineHistory(RecencyHistory[str]):
    """The history for the command line."""


##############################################################################
def command_history_file() -> Path:
    """Get the path for the command history file.

    Returns:
        The path for the command history file.
    """
    return data_dir() / "command-history.json"


##############################################################################
def save_command_history(history: CommandLineHistory) -> None:
    """Save the command history to storage.

    Args:
        history: The command history to save.
    """
    command_history_file().write_text(
        dumps(list(history), indent=4),
        encoding="utf-8",
    )


##############################################################################
def load_command_history() -> CommandLineHistory:
    """Load the command history from storage.

    Returns:
        The loaded command history.
    """
    return CommandLineHistory(
        loads(history.read_text(encoding="utf-8"))
        if (history := command_history_file()).exists()
        else []
    )


### command_history.py ends here
