"""Provides a safer version of Textual's escape"""

##############################################################################
# Python imports.
from re import compile

##############################################################################
# Textual imports.
from textual.markup import escape as borked_escape

##############################################################################
_ESCAPE_SUB_METHOD = compile(r"(\\*)(\[[a-zA-Z#/@][^[]*?])").sub
"""Tweaked version of the original Textual escape function's regexp.

In Textual it just handles lowercase letters and #/@, but in the real world,
we need to handle uppercase letters too, at least.
"""


##############################################################################
def escape(text: str) -> str:
    """Escape text for use in Textual markup.

    Args:
        text: The text to escape.

    Returns:
        The escaped text.
    """
    # Use the original escape function from Textual, but replace the
    # problematic regexp with something approaching behaviour suitable for
    # real world data.
    return borked_escape(text, _ESCAPE_SUB_METHOD)


### safe_escape.py ends here
