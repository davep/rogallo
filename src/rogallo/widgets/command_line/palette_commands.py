"""Palette commands for the command line widget."""

##############################################################################
# Python imports.
from inspect import getmembers, isclass

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import Command

##############################################################################
# Local imports.
from ... import commands
from .base_command import InputCommand


##############################################################################
class PaletteCommand(InputCommand):
    """Change the color palette of the application."""

    @classmethod
    def handle(cls, text: str, for_widget) -> bool:
        """Handle the command.

        Args:
            text: The text of the command.
            for_widget: The widget to handle the command for.

        Returns:
            `True` if the command was handled; `False` if not.
        """
        candidates = {
            f"!{command.action_name().removesuffix('_command')}": command
            for _, command in getmembers(commands, isclass)
            if issubclass(command, Command)
        }
        if text in candidates:
            for_widget.screen.call_next(
                for_widget.screen.run_action, candidates[text].action_name()
            )
            return True
        return False


### palette_commands.py ends here
