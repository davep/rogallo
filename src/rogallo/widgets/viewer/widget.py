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
from textual.containers import HorizontalGroup, Vertical
from textual.events import DescendantBlur, DescendantFocus, Key
from textual.getters import query_one
from textual.reactive import var
from textual.timer import Timer
from textual.widgets import Static

##############################################################################
# Textual enhanced imports.
from textual_enhanced.binding import HelpfulBinding

##############################################################################
# Wasat imports.
from wasat import GeminiURI

##############################################################################
# Local imports.
from ...data import LocationHistory, load_configuration
from ...document import Document
from .content_filter import GemtextContent
from .document_view import DocumentView
from .gemtext_blocks import GemtextLink, get_block_widget
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

        #document-wrapper {
            align-horizontal: center;
        }

        &.--has-content {
            visibility: visible;
        }

        &.--stripe-links GemtextLink {
            background: $background 20%;
            &.--stripe {
                background: $background 60%;
            }
        }

        &.--with-link-numbers GemtextLink #jump {
            display: block;
        }

        &.--cosy-link-numbers GemtextLink #jump {
            dock: left;
            padding-right: 1;
        }
    }
    """

    HELP = """
    As well as the normal widget navigation keys, the following keys are
    available to navigate through the links:
    """

    BINDINGS = [
        HelpfulBinding(
            "left, shift+up, L",
            "previous_link",
            tooltip="Move backwards through each of the links",
        ),
        HelpfulBinding(
            "right, shift+down, l",
            "next_link",
            tooltip="Move forward through each of the links",
        ),
    ]

    document: var[Document] = var(Document(), toggle_class="--has-content")
    """The details of the document to show in the viewer."""
    view_source: var[bool] = var(False)
    """Whether the viewer is showing the source of the document or not."""
    with_link_numbers: var[bool] = var(False, toggle_class="--with-link-numbers")
    """Whether the viewer is showing link numbers or not."""
    cosy_link_numbers: var[bool] = var(False, toggle_class="--cosy-link-numbers")
    """Whether the viewer is showing link numbers in a cosy way or not."""
    stripe_links: var[bool] = var(False, toggle_class="--stripe-links")
    """Whether the viewer is showing links with stripes or not."""
    location_history: var[LocationHistory] = var(LocationHistory)
    """The location history for the viewer."""
    handle_ansi_escape_sequences: var[bool] = var(True)
    """Whether the viewer is handling ANSI escape sequences or not."""
    strip_emoji: var[bool] = var(False)
    """Whether the viewer is stripping emoji or not."""

    _title = query_one(ViewerTitle)
    """The title widget."""
    _view = query_one(DocumentView)
    """The document view widget."""
    _status = query_one(ViewerStatus)
    """The status bar widget."""

    _jump: var[int | None] = var(None)
    """Keeps track of the jump progress."""
    _jump_timer: Timer | None = None
    """A timer to reset the jump progress after a short delay."""
    _jump_map: var[dict[int, GemtextLink]] = var(dict)
    """Keeps track of the jump numbers and their corresponding links."""

    def compose(self) -> ComposeResult:
        """Compose the viewer widget."""
        yield ViewerTitle()
        document = DocumentView()
        if (max_width := load_configuration().maximum_document_width) > 0:
            document.styles.max_width = max_width
            yield HorizontalGroup(document, id="document-wrapper", classes="dead-space")
        else:
            yield document
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
        with self.app.batch_update():
            await self._view.remove_children()
            self._jump_map = {}
            await self._view.mount_all(
                [
                    Static(
                        self.document.content.replace(chr(27), "\N{SYMBOL FOR ESCAPE}"),
                        markup=False,
                    )
                ]
                if not self.document.is_gemtext or self.view_source
                else [
                    get_block_widget(line)
                    for line in self._consolidate(
                        Gemtext(self.document.content).content
                    )
                ]
            )
            if self.document.is_gemtext and not self.view_source:
                visited_links = {
                    str(visit.location)
                    for visit in self.location_history
                    if isinstance(visit.location, GeminiURI)
                }
                for jump_number, link in enumerate(self._view.query(GemtextLink)):
                    link.normalise_uri(self.document.location)
                    link.visited = link.normalised_uri in visited_links
                    link.jump_number = jump_number + 1
                    self._jump_map[link.jump_number] = link
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

    def _watch_with_link_numbers(self) -> None:
        """Watch for changes to the with_link_numbers property."""
        self._jump = None

    def _watch_handle_ansi_escape_sequences(self) -> None:
        """Watch for changes to the handle_ansi_escape_sequences property and update the viewer."""
        GemtextContent.set_filter(
            allow_ansi_escape_sequences=self.handle_ansi_escape_sequences,
            strip_emoji=self.strip_emoji,
        )
        self.mutate_reactive(Viewer.document)

    def _watch_strip_emoji(self) -> None:
        """Watch for changes to the strip_emoji property and update the viewer."""
        GemtextContent.set_filter(
            allow_ansi_escape_sequences=self.handle_ansi_escape_sequences,
            strip_emoji=self.strip_emoji,
        )
        self.mutate_reactive(Viewer.document)

    def _watch__jump(self) -> None:
        """Watch for changes to the jump property and update the viewer."""
        if self._jump is not None:
            if (link := self._jump_map.get(self._jump)) is not None:
                link.focus(scroll_visible=True)
            else:
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

    def _reset_jump_timer(self, start_new: bool = False) -> None:
        """Reset the jump timer."""
        if self._jump_timer is not None:
            self._jump_timer.stop()
            self._jump_timer = None
        if start_new:
            self._jump_timer = self.set_timer(
                load_configuration().jump_progress_timeout, self._reset_jump_progress
            )

    def _reset_jump_progress(self) -> None:
        """Reset the jump progress."""
        self._jump = None
        self._reset_jump_timer()

    @on(Key)
    def _jumper(self, event: Key) -> None:
        """Handle jump key presses."""
        if not self.with_link_numbers:
            return
        if event.key.isdigit():
            event.stop()
            self._jump = (self._jump or 0) * 10 + int(event.key)
            self._reset_jump_timer(start_new=True)
        else:
            self._reset_jump_progress()

    def action_previous_link(self) -> None:
        """Focus the previous link."""
        if not (links := self._view.query(GemtextLink)):
            return
        current = self._view.query_one_optional("GemtextLink:focus", GemtextLink)
        if current is None or (current.jump_number and current.jump_number <= 1):
            self._jump = links.last().jump_number
        elif current.jump_number is not None:
            self._jump = current.jump_number - 1

    def action_next_link(self) -> None:
        """Focus the next link."""
        if not (links := self._view.query(GemtextLink)):
            return
        current = self._view.query_one_optional("GemtextLink:focus", GemtextLink)
        if (last := links.last().jump_number) is None:
            return
        if current is None or (current.jump_number and current.jump_number >= last):
            self._jump = 1
        elif current.jump_number is not None:
            self._jump = current.jump_number + 1


### widget.py ends here
