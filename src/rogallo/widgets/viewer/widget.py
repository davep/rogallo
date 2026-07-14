"""Provides the main viewer widget."""

##############################################################################
# Python imports.
from collections.abc import Iterator

##############################################################################
# Gemtext imports.
from gemtext import Gemtext, Line, Paragraph

##############################################################################
# Textual imports.
from textual import on
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.events import DescendantBlur, DescendantFocus, Key
from textual.getters import query_one
from textual.reactive import var
from textual.widgets import Static

##############################################################################
# Local imports.
from ...document import Document
from .document_view import DocumentView
from .gemtext_blocks import GemtextLink, GemtextWidget, get_block_widget
from .status import ViewerStatus
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

    document: var[Document] = var(Document(), toggle_class="--has-content")
    """The details of the document to show in the viewer."""
    view_source: var[bool] = var(False)
    """Whether the viewer is showing the source of the document or not."""

    _title = query_one(ViewerTitle)
    """The title widget."""
    _view = query_one(DocumentView)
    """The document view widget."""
    _status = query_one(ViewerStatus)
    """The status bar widget."""

    _jump: var[int | None] = var(None)
    """Keeps track of the jump progress."""

    def compose(self) -> ComposeResult:
        """Compose the viewer widget."""
        yield ViewerTitle()
        yield DocumentView()
        yield ViewerStatus()

    @staticmethod
    def _consolidate(lines: tuple[Line, ...]) -> Iterator[Line]:
        """Consolidate consecutive paragraphs into a single paragraph.

        Args:
            lines: The lines to consolidate.

        Yields:
            The consolidated lines.
        """
        buffer: list[str] = []
        for line in lines:
            if isinstance(line, Paragraph):
                buffer.append(str(line))
            else:
                if buffer:
                    yield Paragraph("\n".join(buffer))
                    buffer.clear()
                yield line
        if buffer:
            yield Paragraph("\n".join(buffer))

    async def _watch_document(self) -> None:
        """Watch for changes to the document and update the viewer."""
        self._title.needed_certificate = self.document.needed_certificate
        self._title.location = self.document.location
        self._status.mime_type = self.document.mime_type or ""
        await self._view.remove_children()
        blocks: list[Static] | list[GemtextWidget]
        if not self.document.is_gemtext or self.view_source:
            blocks = [
                Static(
                    self.document.content.replace(chr(27), "\N{SYMBOL FOR ESCAPE}"),
                    markup=False,
                )
            ]
        else:
            blocks = [
                get_block_widget(line)
                for line in self._consolidate(Gemtext(self.document.content).content)
            ]
        await self._view.mount_all(blocks)
        for jump_number, link in enumerate(self._view.query(GemtextLink)):
            link.normalise_uri(self.document.location)
            link.jump_number = jump_number + 1
        # This next bit of nonsense is because Textual fails to sort its
        # scrollbars out upon clearing down and remounting a new set of
        # children. So we have to force it to refresh and then scroll to the
        # end and home to get it to sort itself out. I have this feeling
        # I've reported this before, although I can't find the issue back
        # now. Not that it matters, issues seem to be ignored these days.
        self.call_after_refresh(self._view.scroll_end, animate=False, immediate=True)
        self.call_after_refresh(self._view.scroll_home, animate=False, immediate=True)

    def _watch_view_source(self) -> None:
        """Watch for changes to the view_source property and update the viewer."""
        self.mutate_reactive(Viewer.document)

    def _watch__jump(self) -> None:
        """Watch for changes to the jump property and update the viewer."""
        if self._jump is not None:
            for link in self._view.query(GemtextLink):
                if link.jump_number == self._jump:
                    self._view.scroll_to_widget(link, animate=True)
                    link.focus()
                    return
            self._jump = self._jump % 10 if self._jump > 9 else None

    def take_control(self) -> None:
        """Take control of the UI."""
        self._view.focus()

    @on(DescendantFocus)
    def _maybe_update_status(self, event: DescendantFocus) -> None:
        """Update the status bar when a descendant widget is focused."""
        if isinstance(event.widget, GemtextLink):
            self._status.message = str(event.widget.normalised_uri)
        else:
            self._status.message = ""

    @on(DescendantBlur)
    def _maybe_clear_status(self) -> None:
        """Clear the status bar when a descendant widget is blurred."""
        if self.screen.focused and self not in self.screen.focused.ancestors:
            self._status.message = ""

    @on(Key)
    def _jumper(self, event: Key) -> None:
        """Handle jump key presses."""
        if event.key.isdigit():
            event.stop()
            self._jump = (self._jump or 0) * 10 + int(event.key)
        else:
            self._jump = None


### widget.py ends here
