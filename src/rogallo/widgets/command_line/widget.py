"""Provides the command line for the application."""

##############################################################################
# Python future imports.
from __future__ import annotations

##############################################################################
# Python imports.
from dataclasses import dataclass
from itertools import chain, cycle
from typing import Final

##############################################################################
# Textual imports.
from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.getters import query_one
from textual.message import Message
from textual.reactive import var
from textual.suggester import SuggestFromList
from textual.timer import Timer
from textual.widgets import Input, Label
from textual.widgets.input import Selection

##############################################################################
# Textual enhanced imports.
from textual_enhanced.binding import HelpfulBinding
from textual_enhanced.commands import Quit

##############################################################################
# Wasat imports.
from wasat import GeminiURI

##############################################################################
# Local imports.
from ...data import Bookmarks, CommandLineHistory, LocationHistory, NavigationHistory
from ...types import short_location
from .base_command import InputCommand
from .general import ChangeThemeCommand, HelpCommand, QuitCommand, UnknownCommand
from .open_file import OpenFileCommand
from .open_gemini_uri import OpenGeminiURICommand
from .open_other_uri import OpenOtherURICommand
from .palette_commands import PaletteCommand

##############################################################################
COMMANDS: Final[tuple[type[InputCommand], ...]] = (
    HelpCommand,
    QuitCommand,
    ChangeThemeCommand,
    PaletteCommand,
    UnknownCommand,
    OpenFileCommand,
    OpenGeminiURICommand,
    OpenOtherURICommand,
)
"""The commands used for the input."""

##############################################################################
_PROMPT: Final[str] = ">"
"""The prompt for the command line."""

##############################################################################
_BUSY_CELLS: Final[cycle[str]] = cycle("⠁⠉⠘⠰⠤⠤⠆⠃⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏⠟⠿⠽⠾⠽⠿⠟⠯⠽⠾⠶⠦⠤⠤⠰⠘⠉⠁")
"""The cells used for the busy indicator."""


##############################################################################
class CommandLine(Vertical):
    """The command line for the application."""

    DEFAULT_CSS = """
    CommandLine {
        height: 1;

        Label, Input {
            color: $text-muted;
        }

        Label {
            padding-right: 1;
        }

        &:focus-within {
            Label, Input {
                color: $text;
            }
            Label {
                text-style: bold;
            }
        }

        Input, Input:focus {
            border: none;
            padding: 0;
            height: 1fr;
            background: transparent;
        }

        &.--top {
            dock: top;
        }
    }
    """

    HELP = """
    ## Command Line

    Use this command line to enter filenames, directories, URLs or commands. Entering
    a filename or a URL will open that file for viewing; entering a
    directory will open a file opening dialog starting at that location.

    | Command | Aliases | Description |
    | --      | --      | --          |
    {cli_commands}

    ### Special keys

    Special keys while in the command line:
    """.format(
        cli_commands="\n    ".join(
            sorted(chain(*(command.help_text() for command in COMMANDS)))
        ),
    )

    BINDINGS = [
        ("escape", "request_exit"),
        HelpfulBinding(
            "up",
            "history_previous",
            tooltip="Navigate backwards through the command history",
        ),
        HelpfulBinding(
            "down",
            "history_next",
            tooltip="Navigate forward through the command history",
        ),
    ]

    dock_top: var[bool] = var(False, toggle_class="--top", init=True)
    """Should the input dock to the top of the screen?"""

    working: var[bool] = var(False)
    """Is the command line currently working on something?"""

    history: var[CommandLineHistory] = var(CommandLineHistory)
    """The history for the command line."""

    location_history: var[LocationHistory] = var(LocationHistory)
    """The history of locations visited."""
    navigation_history: var[NavigationHistory] = var(NavigationHistory)
    """The history of navigation through locations."""
    bookmarks: var[Bookmarks] = var(list)
    """The bookmarks for the application."""
    known_hosts: var[list[GeminiURI]] = var(list)
    """The hosts known to the application."""

    _input = query_one(Input)
    """The input widget for the command line."""
    _prompt = query_one(Label)
    """The prompt widget for the command line."""

    _busy_timer: var[Timer | None] = var(None)
    """The timer for the busy indicator."""

    @property
    def _history_suggester(self) -> SuggestFromList:
        """A suggester for the history of input.

        If there us no history yet then a list of commands and aliases will
        be used.
        """
        return SuggestFromList(
            [
                # Start off with the history, with the most recently-used
                # commands first so suggestions come from the thing
                # most-recently done.
                *reversed(list(self.history)),
                # Let's also splice in the other histories and bookmarks so
                # that the user can get suggestions for those too.
                *sorted(
                    set(
                        chain(
                            (str(visit.location) for visit in self.location_history),
                            (str(visit) for visit in self.navigation_history),
                            (str(bookmark.location) for bookmark in self.bookmarks),
                            (str(known_host) for known_host in self.known_hosts),
                            (
                                short_location(visit.location)
                                for visit in self.location_history
                            ),
                            (
                                short_location(visit)
                                for visit in self.navigation_history
                            ),
                            (
                                short_location(bookmark.location)
                                for bookmark in self.bookmarks
                            ),
                            (
                                short_location(known_host)
                                for known_host in self.known_hosts
                            ),
                        )
                    )
                ),
                # Tack known commands on the end; this means that the user
                # will get prompted for commands they've not used yet.
                *chain(*(command.suggestions() for command in COMMANDS)),
            ]
        )

    def compose(self) -> ComposeResult:
        """Compose the content of the widget."""
        with Horizontal():
            yield Label(_PROMPT)
            yield Input(
                placeholder="Enter a URI, file, or command",
                suggester=self._history_suggester,
            )

    @property
    def has_control(self) -> bool:
        """Does the command line have control of the input?"""
        return self._input.has_focus

    @dataclass
    class CommandExecuted(Message):
        """Message posted when a command is executed."""

        command_line: CommandLine
        """The command line whose history was updated."""
        command: str
        """The command that was executed."""

    def _refresh_suggestions(self) -> None:
        """Refresh the suggestions for the input."""
        if self.is_mounted:
            self._input.suggester = self._history_suggester

    def handle_input(self, command: str) -> None:
        """Handle input from the user.

        Args:
            command: The command the user entered.
        """
        if not (command := command.strip()):
            return
        for candidate in COMMANDS:
            if candidate.handle(command, self):
                self.history.add(command)
                self.post_message(self.CommandExecuted(self, command))
                self._input.value = ""
                self._refresh_suggestions()
                return
        self.notify("Unable to handle that input", title="Error", severity="error")

    @on(Input.Submitted)
    def _handle_input(self, message: Input.Submitted) -> None:
        """Handle input from the user.

        Args:
            message: The message requesting input is handled.
        """
        message.stop()
        self.handle_input(message.value)

    def _watch_history(self) -> None:
        """React to history being updated."""
        self._refresh_suggestions()

    def _watch_location_history(self) -> None:
        """React to the location history being updated."""
        self._refresh_suggestions()

    def _watch_navigation_history(self) -> None:
        """React to the navigation history being updated."""
        self._refresh_suggestions()

    def _watch_bookmarks(self) -> None:
        """React to the bookmarks being updated."""
        self._refresh_suggestions()

    def _watch_working(self) -> None:
        """React to the working state being updated."""
        if self.working:
            self._busy_timer = self.set_interval(
                0.1,
                lambda: self._prompt.update(next(_BUSY_CELLS)),
            )
        elif self._busy_timer:
            self._busy_timer.stop()
            self._busy_timer = None
            self._prompt.update(_PROMPT)

    def action_request_exit(self) -> None:
        """Request that the application quits."""
        if self._input.value:
            self._input.value = ""
            self.history.goto_end()
        else:
            self.post_message(Quit())

    def action_history_previous(self) -> None:
        """Move backwards through the command line history."""
        if self._input.value and self.history.can_go_backward:
            self.history.backward()
        if value := (self.history.current_item or ""):
            self._input.value = value
            self._input.selection = Selection(0, len(value))

    def action_history_next(self) -> None:
        """Move forwards through the command line history."""
        if self.history.forward() and (value := self.history.current_item) is not None:
            self._input.value = value
            self._input.selection = Selection(0, len(value))
        else:
            self._input.value = ""


### command_line.py ends here
