"""Support tools for syntax highlighting."""

##############################################################################
# Python imports.
from functools import cache

##############################################################################
# Pygments imports.
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound


##############################################################################
@cache
def supported_language(language: str) -> bool:
    """Check if a language is supported by Pygments.

    Args:
        language: The language to check.

    Returns:
        True if the language is supported; False otherwise.
    """
    try:
        _ = get_lexer_by_name(language)
        return True
    except ClassNotFound:
        return False


### languages.py ends here
