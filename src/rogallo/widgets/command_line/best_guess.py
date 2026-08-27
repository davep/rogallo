"""Provides a command for making a best guess at what the user wants to do with their input."""

##############################################################################
# Port79 imports.
from port79 import FingerURI
from port79 import URIError as FingerURIError

##############################################################################
# Textual imports.
from textual.widget import Widget

##############################################################################
# Local imports.
from ...messages import OpenLocation
from ...preflight import is_likely_finger_request
from .base_command import InputCommand


##############################################################################
class BestGuessCommand(InputCommand):
    """Make a guess at what the input means"""

    @classmethod
    def handle(cls, text: str, for_widget: Widget) -> bool:
        """Handle the command.

        Args:
            text: The text of the command.
            for_widget: The widget to handle the command for.

        Returns:
            `True` if the command was handled; `False` if not.
        """
        if is_likely_finger_request(text):
            try:
                for_widget.post_message(OpenLocation(FingerURI.from_string(text)))
            except FingerURIError:
                return False
            return True
        return False

    @classmethod
    def help_text(cls) -> tuple[str, ...]:
        """Ensure there is no help text for guessed commands."""
        return ()


### best_guess.py ends here
