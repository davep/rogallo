"""Provides a finger command for the command line."""

##############################################################################
# Port79 imports.
from port79 import FingerURI

##############################################################################
# Textual imports.
from textual.widget import Widget

##############################################################################
# Local imports.
from ...messages import OpenLocation
from .base_command import InputCommand


##############################################################################
class FingerCommand(InputCommand):
    """Perform user information looking with the finger protocol"""

    COMMAND = "`!finger`"
    ALIASES = "`!f`"
    ARGUMENTS = "`<user>[@<host>]`"

    @classmethod
    def handle(cls, text: str, for_widget: Widget) -> bool:
        """Handle the command.

        Args:
            text: The text of the command.
            for_widget: The widget to handle the command for.

        Returns:
            `True` if the command was handled; `False` if not.
        """
        command, user = cls.split_command(text)
        if cls.is_command(command):
            for_widget.post_message(OpenLocation(FingerURI.from_string(user)))
            return True
        return False


### finger.py ends here
