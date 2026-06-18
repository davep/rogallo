"""The viewer widget for Rogallo."""

##############################################################################
# Textual imports.
from textual.containers import Vertical
from textual.reactive import var


##############################################################################
class Viewer(Vertical):
    """The viewer widget for Rogallo."""

    DEFAULT_CSS = """
    Viewer {
        height: 1fr;
        width: 1fr;
        visibility: hidden;

        &.--has-document {
            visibility: visible;
        }
    }
    """

    document: var[str] = var("", toggle_class="--has-document")
    """The document to display in the viewer."""


### viewer.py ends here
