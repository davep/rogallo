"""Provides a command for browsing for a gemtext file in the local filesystem."""

##############################################################################
# Python imports.
from pathlib import Path

##############################################################################
# Textual imports.
from textual.widget import Widget

##############################################################################
# Local imports.
from ...messages import OpenFromFileSystem
from .base_command import InputCommand


##############################################################################
class OpenDirectoryCommand(InputCommand):
    """Open `<dir>` and browse for a file to view"""

    COMMAND = "`<dir>`"

    @classmethod
    def handle(cls, text: str, for_widget: Widget) -> bool:
        """Handle the command.

        Args:
            text: The text of the command.
            for_widget: The widget to handle the command for.

        Returns:
            `True` if the command was handled; `False` if not.
        """
        if (start_directory := Path(text).expanduser()).is_dir():
            for_widget.post_message(OpenFromFileSystem(start_directory))
            return True
        return False


### open_directory.py ends here
