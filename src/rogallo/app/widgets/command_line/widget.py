"""Provides the command line for the application."""

##############################################################################
# Python imports.
from typing import Final

##############################################################################
# Textual imports.
from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.reactive import var
from textual.widgets import Input, Label, Rule

##############################################################################
# Local imports.
from .base_command import InputCommand
from .open_gemini_uri import OpenGeminiURICommand

##############################################################################
COMMANDS: Final[tuple[type[InputCommand], ...]] = (OpenGeminiURICommand,)
"""The commands used for the input."""


##############################################################################
class CommandLine(Vertical):
    """The command line for the application."""

    DEFAULT_CSS = """
    CommandLine {
        height: 1;

        Label, Input {
            color: $text-muted;
        }

        &:focus-within {
            Label, Input {
                color: $text;
            }
            Label {
                text-style: bold;
            }
        }

        Rule {
            height: 1;
            margin: 0 !important;
            color: $foreground 10%;
            display: none;
        }

        Input, Input:focus {
            border: none;
            padding: 0;
            height: 1fr;
            background: transparent;
        }

        &.--top {
            dock: top;
            height: 2;
            Rule {
                display: block;
            }
        }
    }
    """

    dock_top: var[bool] = var(False, toggle_class="--top", init=True)
    """Should the input dock to the top of the screen?"""

    def compose(self) -> ComposeResult:
        """Compose the content of the widget."""
        with Horizontal():
            yield Label("> ")
            yield Input(
                placeholder="Enter a URI, file, or command",
            )
        yield Rule(line_style="heavy")

    def handle_input(self, command: str) -> None:
        """Handle input from the user.

        Args:
            command: The command the user entered.
        """
        if not (command := command.strip()):
            return
        for candidate in COMMANDS:
            if candidate.handle(command, self):
                self.query_one(Input).value = ""
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


### command_line.py ends here
