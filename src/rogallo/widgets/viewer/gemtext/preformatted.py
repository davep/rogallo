"""Provides a widget for displaying a block of preformatted text."""

##############################################################################
# Python imports.
from functools import cache

##############################################################################
# Gemtext imports.
from gemtext import Line, PreFormatted

##############################################################################
# Textual imports.
from textual.app import ComposeResult
from textual.highlight import HighlightTheme, highlight
from textual.widgets import Label, Static

##############################################################################
# Local imports.
from ....data import load_configuration
from ..languages import supported_language
from .content_filter import GemtextContent


##############################################################################
@cache
def _blended_types() -> set[str]:
    """Get the set of preformatted types that should be blended with the background.

    Returns:
        The set of preformatted types that should be blended with the background.
    """
    return set(
        alt_text.casefold()
        for alt_text in load_configuration().blend_pre_formatted_with_background
    )


##############################################################################
class GemtextPreformatted(Static):
    """A widget for displaying a Gemtext preformatted text block."""

    DEFAULT_CSS = """
    GemtextPreformatted {
        margin: 0 2;
        overflow: auto;
        &.--highlight {
            background: black 35%;
            &:light {
                background: white 35%;
            }
        }
    }
    """

    def __init__(self, preformatted: Line) -> None:
        """Initialize a Gemtext preformatted text widget.

        Args:
            preformatted: The Gemtext preformatted text to display.
        """
        assert isinstance(preformatted, PreFormatted)
        text = GemtextContent.ansi_filter(preformatted)
        super().__init__(
            highlight(
                str(text),
                language=preformatted.alt_text,
                theme=HighlightTheme,
            )
            if preformatted.has_alt_text and supported_language(preformatted.alt_text)
            else text,
            classes=(
                ""
                if preformatted.alt_text.casefold() in _blended_types()
                else "--highlight"
            ),
        )
        self.tooltip = (
            preformatted.alt_text
            if preformatted.has_alt_text
            and load_configuration().show_preformat_tooltips
            else None
        )


### preformatted.py ends here
