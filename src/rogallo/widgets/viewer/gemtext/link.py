"""Provides a widget for displaying a Gemtext link."""

##############################################################################
# Python imports.
from functools import cached_property
from pathlib import Path
from urllib.parse import urlparse

##############################################################################
# Gemtext imports.
from gemtext import Line, Link

##############################################################################
# Rich imports.
from rich.table import Table
from rich.text import Text

##############################################################################
# Textual imports.
from textual import on
from textual.events import Click
from textual.reactive import reactive, var
from textual.widget import Widget

##############################################################################
# Textual enhanced imports.
from textual_enhanced.binding import HelpfulBinding

##############################################################################
# Local imports.
from ....data import load_configuration
from ....messages import OpenLocation, OpenURI
from ....preflight import (
    has_navigable_path,
    is_finger_uri,
    is_gopher_uri,
    is_likely_capsule,
    is_local_gemtext_file,
    is_nex_uri,
    is_spartan_uri,
)
from ....safe_escape import escape
from ....types import RogalloLocation, SpartanURINeedingData
from .content_filter import GemtextContent
from .icons import icon


##############################################################################
class GemtextLink(Widget, can_focus=True):
    """A widget for displaying a Gemtext link."""

    COMPONENT_CLASSES = {
        "gemtext-link--icon",
        "gemtext-link--jump-number",
    }

    DEFAULT_CSS = """
    GemtextLink {
        margin: 0 1 0 0;
        height: auto;
        pointer: pointer;

        & > .gemtext-link--icon {
            color: $text-primary;
        }

        &.--visited > .gemtext-link--icon {
            color: $text-primary 50%;
        }

        & > .gemtext-link--jump-number {
            color: $text-muted 30%;
        }

        &:hover {
            background: $block-hover-background !important;
        }

        &:focus {
            color: $block-cursor-foreground;
            background: $block-cursor-background !important;
        }
    }
    """

    HELP = """
    ## Link

    This is a link to either another document, or an external resource that
    will be handled by your system.
    """

    BINDINGS = [HelpfulBinding("enter", "open_link", "Open link", show=False)]

    visited: var[bool] = var(False, toggle_class="--visited")
    """Whether the link has been visited or not."""
    with_link_numbers: reactive[bool] = reactive(True)
    """Whether to show link numbers or not."""
    cosy_link_numbers: reactive[bool] = reactive(False)
    """Whether to show link numbers in a cosy way or not."""
    jump_number: reactive[int | None] = reactive(None)
    """The jump number for the link."""

    _normalised_uri: reactive[str] = reactive("")
    """The normalised URI to use when opening the link."""

    def __init__(self, link: Line) -> None:
        """Initialize a Gemtext link widget.

        Args:
            line: The Gemtext link to display.
        """
        super().__init__()
        assert isinstance(link, Link)
        self._link = link
        """The link data."""
        self._normalised_uri = link.uri
        """The normalised URI to use when opening the link."""
        self._filtered_content: Text | str | None = None
        """The filtered content of the link."""

    @property
    def normalised_uri(self) -> str:
        """The normalised URI to use when opening the link."""
        return self._normalised_uri

    @cached_property
    def _best_icon(self) -> str:
        """Get the best icon for the link based on its URI."""
        for checker, icon_name in (
            (is_likely_capsule, "geminispace_link_icon"),
            (is_finger_uri, "fingerspace_link_icon"),
            (is_gopher_uri, "gopherspace_link_icon"),
            (is_spartan_uri, "spartanspace_link_icon"),
            (is_nex_uri, "nexspace_link_icon"),
            (is_local_gemtext_file, "geminispace_link_icon"),
        ):
            if checker(self.normalised_uri):
                return icon(icon_name)
        return icon("otherspace_link_icon")

    def normalise_uri(self, base_uri: RogalloLocation | None) -> None:
        """Normalise the URI of the link against a base URI.

        Args:
            base_uri: The base URI to normalise against.
        """
        if base_uri is None:
            return
        if urlparse(self._normalised_uri).scheme:
            return
        if has_navigable_path(base_uri):
            self._normalised_uri = str(base_uri.resolve(self._link.uri))
        elif isinstance(base_uri, Path):
            self._normalised_uri = (base_uri.parent / self._link.uri).resolve().as_uri()

    def _watch__normalised_uri(self) -> None:
        """Watch for changes to the normalised URI."""
        if load_configuration().show_link_tooltips:
            self.tooltip = self._normalised_uri

    @property
    def _jump_link_content(self) -> str | Text:
        """Get the content for the jump link."""
        return (
            ""
            if self.jump_number is None
            else Text(
                escape(f"[{self.jump_number}]"),
                style=self.get_component_rich_style("gemtext-link--jump-number"),
            )
        )

    def _watch_jump_number(self) -> None:
        """Watch for changes to the jump number."""
        self.set_class(
            self.jump_number is not None and not bool(self.jump_number % 2),
            "--stripe",
        )

    def render(self) -> Table:
        """Render the Gemtext link widget."""
        link = Table.grid(expand=True)
        link_jump: str | Text = (
            self._jump_link_content if self.with_link_numbers else ""
        )

        # Icon is always first.
        link.add_column(width=2)
        link_data: list[str | Text] = [
            Text(
                self._best_icon,
                style=self.get_component_rich_style("gemtext-link--icon"),
            )
        ]

        # Next is the link number, if we're showing them and they're "cosy".
        if self.with_link_numbers and self.cosy_link_numbers:
            link.add_column(width=len(link_jump) + 1)
            link_data.append(link_jump)

        # Now the link text.
        link.add_column(ratio=1)
        if self._filtered_content is None:
            self._filtered_content = GemtextContent.filter(self._link)
        link_data.append(self._filtered_content)

        # If we're showing link numbers and they're not "cosy".
        if self.with_link_numbers and not self.cosy_link_numbers:
            link.add_column(width=len(link_jump) + 1, justify="right")
            link_data.append(link_jump)

        link.add_row(*link_data)
        return link

    def _navigate_to_uri(self) -> None:
        """Navigate to the normalised URI."""
        self.post_message(OpenURI(self._normalised_uri, allow_cached=False))

    @on(Click)
    def _action_open_link(self) -> None:
        """Open the link."""
        self._navigate_to_uri()


##############################################################################
class SpartanPromptLink(GemtextLink):
    """A widget for displaying a Gemtext link that is a Spartan prompt."""

    def _navigate_to_uri(self) -> None:
        """Navigate to the normalised URI."""
        self.post_message(
            OpenLocation(
                SpartanURINeedingData(self._normalised_uri),
                allow_cached=False,
                avoid_history=True,
            )
        )


### link.py ends here
