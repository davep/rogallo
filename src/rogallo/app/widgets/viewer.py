"""The viewer widget for Rogallo."""

##############################################################################
# Textual imports.
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.getters import query_one
from textual.reactive import var
from textual.widgets import Static


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

    _document = query_one("#document", Static)

    def compose(self) -> ComposeResult:
        yield Static(id="document")

    def _watch_document(self) -> None:
        self._document.update(self.document)


### viewer.py ends here
