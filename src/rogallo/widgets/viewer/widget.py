"""Provides the main viewer widget."""

##############################################################################
# Python imports.
from collections.abc import Iterator
from functools import cached_property

##############################################################################
# Gemtext imports.
from gemtext import Gemtext, Line, Paragraph, PreFormatted

##############################################################################
# html2gemtext imports.
from html2gemtext import html_to_gemtext

##############################################################################
# Port79 imports.
from port70 import GopherURI
from port79 import FingerURI

##############################################################################
# Rich imports.
from rich.text import Text

##############################################################################
# Sybaritic imports.
from sybaritic import SpartanURI

##############################################################################
# Textual imports.
from textual import on
from textual.app import ComposeResult
from textual.containers import HorizontalGroup, Vertical
from textual.events import DescendantBlur, DescendantFocus, Key
from textual.getters import query_one
from textual.highlight import HighlightTheme, highlight
from textual.reactive import var
from textual.timer import Timer
from textual.widget import Widget
from textual.widgets import Markdown, Static

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
from ...types import GEMINI_MIME_TYPE
from .document_view import DocumentView
from .gemtext import GemtextContent, GemtextLink, get_block_widget
from .gopher import to_gemtext
from .languages import language_from_document
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
            height: 1fr;
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

    _WITH_SOURCE_MIME_TYPES = frozenset(
        {
            GEMINI_MIME_TYPE,
            "text/markdown",
            "text/x-markdown",
            "text/html",
        }
    )
    """The MIME types that can be viewed as source."""

    @property
    def can_view_source(self) -> bool:
        """Whether the viewer can view the source of the document.

        Returns:
            Whether the viewer can view the source of the document.
        """
        return self.document.mime_type_sans_parameters in self._WITH_SOURCE_MIME_TYPES

    @cached_property
    def _hidden_pre_alt_text(self) -> set[tuple[str, str]]:
        """Get the set of preformatted types that should be hidden.

        Returns:
            The set of preformatted types that should be hidden.
        """
        cleaned = (
            entry
            for entry in load_configuration().hide_preformatted
            if len(entry) == 2 and all(isinstance(element, str) for element in entry)
        )
        return set(
            (uri_prefix.casefold(), alt_text.casefold())
            for uri_prefix, alt_text in cleaned
        )

    def _gemtext_widgets(
        self, content: str, with_spartan_support: bool = False
    ) -> list[Widget]:
        """Build a list of widgets to display the Gemtext content.

        Args:
            content: The content to convert.
            with_spartan_support: Whether to support Spartan links.

        Returns:
            The widgets for the Gemtext content.
        """
        current_location = (
            str(self.document.location).casefold() if self.document.location else ""
        )
        # Get the set of alt_texts to ignore based on the current location.
        alt_text_to_ignore = {
            alt_text
            for uri_prefix, alt_text in self._hidden_pre_alt_text
            if self.document.location and current_location.startswith(uri_prefix)
        }
        return [
            get_block_widget(line)
            for line in self._consolidate(
                Gemtext(
                    content,
                    with_spartan_support=with_spartan_support,
                ).content
            )
            # Filter out any preformatted blocks that have an alt text we
            # should ignore.
            if not (
                isinstance(line, PreFormatted)
                and line.alt_text.casefold() in alt_text_to_ignore
            )
        ]

    _MARKDOWN_MIME_TYPES = frozenset(
        {
            "text/markdown",
            "text/x-markdown",
        }
    )
    """The MIME types that can be viewed as Markdown."""

    def _best_presentation_for(self, document: Document) -> list[Widget]:
        """Get the best presentation for the document.

        Args:
            document: The document to get the best presentation for.

        Returns:
            The best presentation for the document.
        """
        if not self.view_source:
            if document.mime_type_sans_parameters in self._MARKDOWN_MIME_TYPES:
                return [Markdown(document.content)]
            if document.mime_type_sans_parameters == "text/html":
                return self._gemtext_widgets(html_to_gemtext(document.content))
        return [
            Static(
                Text.from_ansi(document.content)
                if "\x1b[" in document.content
                else highlight(
                    document.content,
                    language=language_from_document(document),
                    theme=HighlightTheme,
                ),
                markup=False,
            )
        ]

    def _build_content(self) -> list[Widget]:
        """Build the content for the viewer.

        Returns:
            The content for the viewer based on the current document.
        """
        if self.document.is_renderable_as_gemtext:
            if self.view_source:
                return [
                    Static(
                        self.document.content.replace(chr(27), "\N{SYMBOL FOR ESCAPE}"),
                        markup=False,
                    )
                ]
            return self._gemtext_widgets(
                self.document.content
                if self.document.is_gemtext
                else "\n".join(to_gemtext(self.document.content)),
                with_spartan_support=isinstance(self.document.location, SpartanURI),
            )
        return self._best_presentation_for(self.document)

    async def _watch_document(
        self, old_document: Document, new_document: Document
    ) -> None:
        """Watch for changes to the document and update the viewer.

        Args:
            old_document: The old document.
            new_document: The new document.
        """
        if old_document.location != new_document.location:
            self.set_reactive(Viewer.view_source, False)
        self._title.verification_method = self.document.verification_method
        self._title.needed_certificate = self.document.needed_certificate
        self._title.location = self.document.location
        self._status.mime_type = self.document.mime_type or ""
        self._jump_map = {}
        with self.app.batch_update():
            await self._view.remove_children()
            await self._view.mount_all(self._build_content())
            if (
                self.document.is_gemtext or self.document.is_gophermap
            ) and not self.view_source:
                visited_links = {
                    str(visit.location)
                    for visit in self.location_history
                    if isinstance(visit.location, (FingerURI, GeminiURI, GopherURI))
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
