"""Provides a command for opening a gemtext file in the local filesystem."""

##############################################################################
# Textual imports.
from textual.widget import Widget

##############################################################################
# Local imports.
from ...messages import OpenLocation
from ...preflight import is_likely_text_file, path_from_uri
from .base_command import InputCommand


##############################################################################
class OpenFileCommand(InputCommand):
    """Open `<file>` as gemtext in the viewer, if it looks like a text file"""

    COMMAND = "`<file>`"

    @classmethod
    def handle(cls, text: str, for_widget: Widget) -> bool:
        """Handle the command.

        Args:
            text: The text of the command.
            for_widget: The widget to handle the command for.

        Returns:
            `True` if the command was handled; `False` if not.
        """
        if is_likely_text_file(text):
            for_widget.post_message(OpenLocation(path_from_uri(text)))
            return True
        return False


### open_file.py ends here
