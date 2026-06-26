"""Provides a command for opening a Gemini URI."""

##############################################################################
# Textual imports.
from textual.widget import Widget

##############################################################################
# Wasat imports.
from wasat import GeminiURI, URIError
from wasat.uri import GEMINI_PREFIX

##############################################################################
# Local imports.
from ...messages import OpenLocation
from ...preflight import is_likely_capsule, is_likely_schemeless_capsule
from .base_command import InputCommand


##############################################################################
class OpenGeminiURICommand(InputCommand):
    """View the document at a `gemini://` `<uri>`"""

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
        try:
            uri = GeminiURI(text)
        except URIError:
            if is_likely_schemeless_capsule(text):
                uri = GeminiURI(f"{GEMINI_PREFIX}{text}")
            else:
                return False
        for_widget.post_message(OpenLocation(uri))
        return True


### open_gemini_uri.py ends here
