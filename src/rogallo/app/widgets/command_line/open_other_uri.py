"""Provides a command for opening a other URIs."""

##############################################################################
# Python imports.
from urllib.parse import urlparse

##############################################################################
# Textual imports.
from textual.widget import Widget

##############################################################################
# Local imports.
from ...messages import OpenURI
from .base_command import InputCommand


##############################################################################
class OpenOtherURICommand(InputCommand):
    """Open `<uri>` in your external browser"""

    COMMAND = "`<uri>`"

    @classmethod
    def handle(cls, text: str, for_widget: Widget) -> bool:
        """Handle the command.

        Args:
            text: The text of the command.
            for_widget: The widget to handle the command for.

        Returns:
            `True` if the command was handled; `False` if not.
        """
        if urlparse(text).scheme:
            for_widget.post_message(OpenURI(text))
            return True
        return False


### open_other_uri.py ends here
