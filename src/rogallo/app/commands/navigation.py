"""Commands related to navigation."""

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import Command


##############################################################################
class Forward(Command):
    """Move forward through history"""

    BINDING_KEY = "ctrl+right_square_bracket"
    SHOW_IN_FOOTER = True


##############################################################################
class Backward(Command):
    """Move backward through history"""

    BINDING_KEY = "ctrl+left_square_bracket"
    SHOW_IN_FOOTER = True


### navigation.py ends here
