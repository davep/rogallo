"""Commands for copying things to the clipboard."""

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import Command


##############################################################################
class CopyLocationToClipboard(Command):
    """Copy the current location to the clipboard."""

    BINDING_KEY = "ctrl+shift+c"


### clipboard.py ends here
