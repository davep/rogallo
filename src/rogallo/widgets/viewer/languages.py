"""Support tools for syntax highlighting."""

##############################################################################
# Python imports.
from functools import cache

##############################################################################
# Pygments imports.
from pygments.lexers import get_lexer_by_name, get_lexer_for_mimetype, guess_lexer
from pygments.util import ClassNotFound

##############################################################################
# Local imports.
from ...data import load_configuration
from ...document import Document


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
    except ClassNotFound:
        return False
    return True


##############################################################################
def language_from_document(document: Document) -> str | None:
    """Try and work out the language of a document.

    Args:
        document: The document to check.

    Returns:
        The language of the document, or None if it could not be determined.
    """
    # Try and work out from the MIME type first.
    if document.mime_type is not None:
        try:
            return get_lexer_for_mimetype(document.mime_type).name.lower()
        except ClassNotFound:
            pass
    # Allow not guessing.
    if not load_configuration().guess_language_for_syntax_highlighting_text_documents:
        return None
    # Failing that, see if we can work out a good guess from the content.
    try:
        return guess_lexer(document.content).name.lower()
    except ClassNotFound:
        return None


### languages.py ends here
