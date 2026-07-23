"""Palette commands for the command line widget."""

##############################################################################
# Python imports.
from inspect import getmembers, isclass

##############################################################################
# Textual imports.
from textual.widget import Widget

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import Command

##############################################################################
# Local imports.
from ... import commands
from .base_command import InputCommand


##############################################################################
class PaletteCommand(InputCommand):
    """Pull command palette commands into the command line."""

    _borrowed_commands: dict[str, type[Command]] | None = None
    """The commands borrowed from the command palette."""

    @classmethod
    def borrowed_commands(cls) -> dict[str, type[Command]]:
        """Get the borrowed commands.

        Returns:
            The borrowed commands.
        """
        if cls._borrowed_commands is None:
            cls._borrowed_commands = {
                f"!{command.action_name().removesuffix('_command')}": command
                for _, command in getmembers(commands, isclass)
                if issubclass(command, Command)
            }
        return cls._borrowed_commands

    @classmethod
    def help_text(cls) -> tuple[str, ...]:
        """Get the help text for the command.

        Returns:
            The help text formatted as Markdown table rows.
        """
        return tuple(
            f"| `{command_name}` | | | {command.__doc__} |"
            for command_name, command in cls.borrowed_commands().items()
        )

    @classmethod
    def suggestions(cls) -> tuple[str, ...]:
        """The suggested command matches for this command.

        Returns:
            A tuple of suggestions for the command.
        """
        return tuple(cls.borrowed_commands().keys())

    @classmethod
    def handle(cls, text: str, for_widget: Widget) -> bool:
        """Handle the command.

        Args:
            text: The text of the command.
            for_widget: The widget to handle the command for.

        Returns:
            `True` if the command was handled; `False` if not.
        """
        if (
            text in cls.borrowed_commands()
            and (screen := for_widget.screen) is not None
        ):
            if screen.check_action(
                action := cls.borrowed_commands()[text].action_name(), ()
            ):
                screen.call_next(screen.run_action, action)
            else:
                screen.notify(
                    "That command isn't available in this context.",
                    title="Not available",
                    severity="warning",
                )
            return True
        return False


### palette_commands.py ends here
