"""Provides the main viewer widget."""

##############################################################################
# Python imports.
from typing import NamedTuple

##############################################################################
# Textual imports.
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.getters import query_one
from textual.reactive import var

##############################################################################
# Local imports.
from ....gemtext import Gemtext
from ...types import GeminiLocation
from .document_view import DocumentView
from .gemtext_blocks import GemtextLink, get_block_widget
from .title import ViewerTitle


##############################################################################
class Viewer(Vertical, can_focus=False):
    """A Gemtext viewer."""

    DEFAULT_CSS = """
    Viewer {
        height: 1fr;
        width: 1fr;
        visibility: hidden;

        &.--has-content {
            visibility: visible;
        }
    }
    """

    class Document(NamedTuple):
        """A named tuple representing details of the document."""

        location: GeminiLocation | None
        """The source of the document."""
        content: str
        """The content of the document."""

        def __bool__(self) -> bool:
            """Return True if the document has content, False otherwise."""
            return bool(self.content)

    document: var[Document] = var(Document(None, ""), toggle_class="--has-content")
    """The details of the document to show in the viewer."""

    _title = query_one(ViewerTitle)
    """The title widget."""
    _view = query_one(DocumentView)
    """The document view widget."""

    def compose(self) -> ComposeResult:
        """Compose the viewer widget."""
        yield ViewerTitle()
        yield DocumentView()

    async def _watch_document(self) -> None:
        """Watch for changes to the document and update the viewer."""
        self._title.location = self.document.location
        await self._view.remove_children()
        for widget in (
            blocks := [
                get_block_widget(line)
                for line in Gemtext(self.document.content).content
            ]
        ):
            if isinstance(widget, GemtextLink):
                widget.normalise_uri(self.document.location)
        await self._view.mount_all(blocks)


### widget.py ends here
