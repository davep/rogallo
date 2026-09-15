"""Provides code for saving and loading the command history."""

##############################################################################
# Python imports.
from json import dumps, loads
from pathlib import Path

##############################################################################
# BogOfStuff imports.
from bagofstuff.history import RecencyHistory

##############################################################################
# Local imports.
from ..locations import data_dir, state_dir


##############################################################################
class CommandLineHistory(RecencyHistory[str]):
    """The history for the command line."""


##############################################################################
def _deprecated_command_history_file() -> Path:
    """Get the path for the deprecated command history file.

    Returns:
        The path for the deprecated command history file.
    """
    return data_dir() / "command-history.json"


##############################################################################
def command_history_file() -> Path:
    """Get the path for the command history file.

    Returns:
        The path for the command history file.
    """
    return state_dir() / "command-history.json"


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
    # BEGIN DEPRECATED SUPPORT
    if (deprecated_history := _deprecated_command_history_file()).exists():
        save_command_history(
            CommandLineHistory(loads(deprecated_history.read_text(encoding="utf-8")))
        )
        deprecated_history.unlink()
    # END DEPRECATED SUPPORT
    return CommandLineHistory(
        loads(history.read_text(encoding="utf-8"))
        if (history := command_history_file()).exists()
        else []
    )


### command_history.py ends here
