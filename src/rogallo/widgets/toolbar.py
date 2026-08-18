"""Provides a toolbar widget that holds command buttons."""

##############################################################################
# Python imports.
from typing import Any

##############################################################################
# Textual imports.
from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.events import Click
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import Label

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import Command
from textual_enhanced.commands.bindings import primary_key_for

##############################################################################
# Local imports.
from .. import __version__, commands


##############################################################################
class CommandButton(Widget):
    """A command button widget that can be clicked to execute a command."""

    DEFAULT_CSS = """
    CommandButton {
        color: $text-muted;
        background: $surface-lighten-2;
        width: auto;
        height: 1;
        pointer: pointer;
        padding: 0 1;
        margin: 0 1;
        &:first-of-type {
            margin-left: 0;
        }
        &:focus {
            color: $text;
            background: $block-cursor-background;
            text-style: bold;
        }
        &:hover {
            color: $text;
            background: $block-hover-background;
            text-style: bold;
        }
        &:disabled {
            text-opacity: 50%;
            opacity: 50%;
        }
    }
    """

    BINDINGS = [("enter", "execute_command", "Execute command")]

    def __init__(
        self,
        command: type[Command],
        title: str | None,
        can_focus: bool = False,
        show_tooltip: bool = False,
    ) -> None:
        """Initialise the command button.

        Args:
            command: The command to execute when the button is clicked.
            title: Optional title for the command.
            can_focus: Whether the button can be focused.
            show_tooltip: Whether to show a tooltip for the button.
        """
        super().__init__()
        self._command = command
        """The command that is executed by this button."""
        self._title = title
        """The title of the button."""
        self._show_tooltip = show_tooltip
        """Whether to show a tooltip for the button."""
        self.can_focus = can_focus

    def render(self) -> str:
        """Render the button."""
        return self._title or self._command().context_command

    def on_mount(self) -> None:
        """Configure the widget once mounted."""
        if self._show_tooltip:
            self.tooltip = f"{self._command().context_tooltip} [$accent]\\[{primary_key_for(self, self._command)}]"
        self.refresh_enabled_state()

    @on(Click)
    async def action_execute_command(self) -> None:
        """Execute the command."""
        await self.screen.run_action(self._command.action_name())

    def refresh_enabled_state(self) -> None:
        """Refresh the enabled state of the button."""
        self.disabled = not bool(
            self.is_mounted
            and self.screen.check_action(self._command.action_name(), ())
        )


##############################################################################
class Toolbar(Horizontal):
    """A toolbar widget that holds command buttons."""

    DEFAULT_CSS = """
    Toolbar {
        height: 1;
        background: $panel;
        color: $foreground;
        #version {
            dock: right;
            padding: 0 1;
            color: $text-muted;
        }
        & > .error {
            color: $error;
            margin: 0 1;
            padding: 0 1;
        }
    }
    """

    def __init__(
        self,
        commands: list[str | list[str]],
        can_focus: bool = False,
        show_tooltips: bool = True,
    ):
        """Initialise the toolbar.

        Args:
            commands: The commands to show in the toolbar.
            can_focus: Whether the toolbar can be focused.
            show_tooltips: Whether to show tooltips for the buttons in the toolbar.
        """
        super().__init__()
        self._can_focus_buttons = can_focus
        """Whether the buttons in the toolbar can be focused."""
        self._show_button_tooltips = show_tooltips
        """Whether to show tooltips for the buttons in the toolbar."""
        self._commands = commands
        """The commands to show in the toolbar."""

    def compose(self) -> ComposeResult:
        """Compose the toolbar."""
        for toolbar_button in self._commands:
            try:
                command_name, title = (
                    toolbar_button
                    if isinstance(toolbar_button, list)
                    else (toolbar_button, None)
                )
            except ValueError:
                yield Label("Error", classes="error").with_tooltip(
                    "Invalid command button configuration item"
                )
                continue
            if command := getattr(commands, command_name, None):
                yield CommandButton(
                    command=command,
                    title=title,
                    can_focus=self._can_focus_buttons,
                    show_tooltip=self._show_button_tooltips,
                )
            else:
                yield Label(command_name, markup=False, classes="error").with_tooltip(
                    f"{command_name} is an unknown command"
                )
        yield Label(f"v{__version__}", id="version")

    def _bindings_updated(self, screen: Screen[Any]) -> None:
        """React to the bindings being updated on the screen.

        Args:
            screen: The screen that has updated bindings.
        """
        if self.is_mounted and screen is self.screen:
            for button in self.query(CommandButton):
                button.refresh_enabled_state()

    def on_mount(self) -> None:
        """Configure the widget once mounted."""
        self.screen.bindings_updated_signal.subscribe(self, self._bindings_updated)

    def on_unmouunt(self) -> None:
        """Clean up the widget when being unmounted."""
        self.screen.bindings_updated_signal.unsubscribe(self)


### toolbar.py ends here
