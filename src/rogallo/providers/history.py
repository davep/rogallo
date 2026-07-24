"""Search and visit history from the command palette."""

##############################################################################
# Python imports.
from dataclasses import dataclass
from functools import total_ordering
from itertools import chain

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import CommandHit, CommandHits, CommandsProvider

##############################################################################
# Wasat imports.
from wasat import GeminiURI

##############################################################################
# Local imports.
from ..data import LocationHistory, LocationVisit, NavigationHistory
from ..messages import OpenLocation
from ..types import RogalloLocation


##############################################################################
class KnownHost(GeminiURI):
    """A known host."""


##############################################################################
@dataclass(frozen=True)
@total_ordering
class Historical:
    """Represents a historical location."""

    location: RogalloLocation | LocationVisit | GeminiURI
    """The historical location."""

    @property
    def name(self) -> str:
        """Get the name of the historical location."""
        if isinstance(self.location, LocationVisit):
            return str(self.location.location)
        return str(self.location)

    @property
    def context(self) -> str:
        """The context for the location."""
        if isinstance(self.location, LocationVisit):
            return f"From history; last visited: {self.location.timestamp.replace(microsecond=0)}"
        if isinstance(self.location, KnownHost):
            return "From known hosts"
        return "From navigation history"

    @property
    def target(self) -> RogalloLocation:
        """Get the target location."""
        if isinstance(self.location, LocationVisit):
            return self.location.location
        return self.location

    def __gt__(self, value: object, /) -> bool:
        if isinstance(value, Historical):
            return self.name.casefold() > value.name.casefold()
        raise NotImplementedError

    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, Historical):
            return self.name.casefold() == value.name.casefold()
        raise NotImplementedError

    def __str__(self) -> str:
        return self.name

    def __hash__(self) -> int:
        return hash(str(self.target))


##############################################################################
class HistorySearchCommands(CommandsProvider):
    """Provides commands for searching and visiting history."""

    navigation_history: NavigationHistory = NavigationHistory()
    """The navigation history."""
    location_history: LocationHistory = LocationHistory()
    """The location history."""
    known_hosts: list[GeminiURI] = []
    """The known hosts."""

    @classmethod
    def prompt(cls) -> str:
        """The prompt for the command provider."""
        return "Search history..."

    def commands(self) -> CommandHits:
        """Provide the commands for searching and visiting history.

        Yields:
            The commands for searching and visiting history.
        """
        for location in sorted(
            set(
                Historical(location)
                for location in chain(
                    self.location_history,
                    self.navigation_history,
                    (KnownHost(host) for host in self.known_hosts),
                )
            )
        ):
            yield CommandHit(
                location.name,
                location.context,
                OpenLocation(location.target),
            )


### history.py ends here
