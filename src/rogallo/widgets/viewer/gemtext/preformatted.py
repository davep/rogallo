"""Provides a widget for displaying a block of preformatted text."""

##############################################################################
# Python imports.
from functools import cache

##############################################################################
# Gemtext imports.
from gemtext import Line, PreFormatted

##############################################################################
# Pygments imports.
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound

##############################################################################
# Textual imports.
from textual.app import ComposeResult
from textual.highlight import HighlightTheme, highlight
from textual.widgets import Label, Static

##############################################################################
# Local imports.
from ....data import load_configuration
from .content_filter import GemtextContent


##############################################################################
@cache
def _supported_language(language: str) -> bool:
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


##############################################################################
class GemtextPreformatted(Static):
    """A widget for displaying a Gemtext preformatted text block."""

    DEFAULT_CSS = """
    GemtextPreformatted {
        margin: 0 2;
        background: black 35%;
        overflow: auto;
        &:light {
            background: white 35%;
        }
    }
    """

    def __init__(self, preformatted: Line) -> None:
        """Initialize a Gemtext preformatted text widget.

        Args:
            preformatted: The Gemtext preformatted text to display.
        """
        assert isinstance(preformatted, PreFormatted)
        self._preformatted = preformatted
        """The Gemtext preformatted text to display."""
        super().__init__()
        self.tooltip = (
            preformatted.alt_text
            if preformatted.has_alt_text
            and load_configuration().show_preformat_tooltips
            else None
        )

    def compose(self) -> ComposeResult:
        """Compose the Gemtext preformatted text widget."""
        text = GemtextContent.ansi_filter(self._preformatted)
        yield Label(
            highlight(
                str(text),
                language=self._preformatted.alt_text,
                theme=HighlightTheme,
            )
            if self._preformatted.has_alt_text
            and _supported_language(self._preformatted.alt_text)
            else text,
            markup=False,
        )


### preformatted.py ends here
