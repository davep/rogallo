"""Provides code for expanding command line aliases."""

##############################################################################
# Python imports.
from string import Formatter
from urllib.parse import quote, quote_plus

##############################################################################
# Local imports.
from ...data import load_configuration


##############################################################################
class AliasError(Exception):
    """An error raised when an alias is invalid."""


##############################################################################
def expand_aliases(command_line: str) -> str:
    """Expand command line aliases.

    Args:
        command_line: The command line to expand.

    Returns:
        The expanded command line.
    """
    aliases = load_configuration().aliases
    car, _, cdr = command_line.partition(" ")
    if car in aliases:
        cdr = cdr.strip()
        try:
            command_line = Formatter().format(
                aliases[car],
                q=quote(cdr),
                qp=quote_plus(cdr),
                r=cdr,
            )
        except KeyError as error:
            raise AliasError(
                f"Alias '{car}' uses an unknown parameter: {error}"
            ) from error
    return command_line


### aliases.py ends here
