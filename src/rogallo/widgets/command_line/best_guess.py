"""Provides a command for making a best guess at what the user wants to do with their input."""

##############################################################################
# Port70 imports.
from port70 import GopherURI
from port70 import URIError as GopherURIError

##############################################################################
# Port79 imports.
from port79 import FingerURI
from port79 import URIError as FingerURIError

##############################################################################
from port1900 import NexURI
from port1900 import URIError as NexURIError

##############################################################################
from sybaritic import SpartanURI
from sybaritic import URIError as SpartanURIError

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
        # Finger is a special case.
        if is_likely_finger_request(text):
            try:
                for_widget.post_message(OpenLocation(FingerURI.from_string(text)))
            except FingerURIError:
                return False
            return True

        # Now let's try and guess based on host names.
        for prefix, uri_class, uri_error in (
            ("gopher", GopherURI, GopherURIError),
            ("spartan", SpartanURI, SpartanURIError),
            ("nex", NexURI, NexURIError),
        ):
            if not text.startswith(f"{prefix}."):
                continue
            try:
                for_widget.post_message(
                    OpenLocation(uri_class.with_default_scheme(text))
                )
            except uri_error:
                continue
            return True
        return False

    @classmethod
    def help_text(cls) -> tuple[str, ...]:
        """Ensure there is no help text for guessed commands."""
        return ()


### best_guess.py ends here
