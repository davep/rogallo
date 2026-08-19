"""Provides code for building a screenshot-ready Rogallo instance."""

import os
from argparse import Namespace
from dataclasses import fields
from datetime import datetime, timedelta
from pathlib import Path
from random import randint
from typing import Any

import port70.uri
import port79.uri
import sybaritic.uri
from wasat import GeminiURI

from rogallo.data import (
    Bookmark,
    CommandLineHistory,
    Configuration,
    LocationHistory,
    LocationVisit,
    NavigationHistory,
    save_bookmarks,
    save_command_history,
    save_location_history,
    save_naviagation_history,
    update_configuration,
)
from rogallo.data.themes import themes_dir
from rogallo.rogallo import Rogallo

##############################################################################
# Patch the ports for Gopher, Finger and Spartan so the screenshots don't
# show non-standard ports.
port70.uri.GOPHER_DEFAULT_PORT = 7070
port79.uri.FINGER_DEFAULT_PORT = 7979
sybaritic.uri.SPARTAN_DEFAULT_PORT = 3000

##############################################################################
# Work our the root of the documentation directory and the build directory.
docs_dir = Path(__file__).parent.parent.parent
docs_build_dir = docs_dir / "build"

##############################################################################
# Set the XDG_ to point at an isolated build environment for the
# screenshots. I don't want to mess with an actual installation of Rogallo.
os.environ["XDG_CACHE_HOME"] = str(docs_build_dir / "cache")
os.environ["XDG_CONFIG_HOME"] = str(docs_build_dir / "config")
os.environ["XDG_DATA_HOME"] = str(docs_build_dir / "data")

##############################################################################
# Create some bookmarks for the screenshots.
save_bookmarks(
    [
        Bookmark("The Gemini Protocol", GeminiURI("gemini://geminiprotocol.net/")),
        Bookmark("davep", GeminiURI("gemini://tilde.team/~davep/")),
        Bookmark("Station", GeminiURI("gemini://station.martinrue.com/")),
        Bookmark("AstroBotany", GeminiURI("gemini://astrobotany.mozz.us/")),
    ]
)

##############################################################################
# Create some sample custom themes.
themes_dir().mkdir(parents=True, exist_ok=True)
for theme in ("white", "amber", "green", "cbm64"):
    (themes_dir() / Path(theme).with_suffix(".json")).write_text(
        (
            Path(__file__).parent.parent.parent.parent
            / "example-themes"
            / Path(theme).with_suffix(".json")
        ).read_text()
    )


##############################################################################
# Create some location history for the screenshots.
def fake_history() -> None:
    save_location_history(
        LocationHistory(
            list(
                reversed(
                    [
                        LocationVisit(
                            GeminiURI.with_default_scheme(location),
                            datetime.now()
                            - timedelta(
                                hours=position,
                                minutes=randint(0, 59),
                                seconds=randint(0, 59),
                            ),
                        )
                        for position, location in enumerate(
                            [
                                "tlgs.one/",
                                "lagrange-point.space/",
                                "station.martinrue.com/davep",
                                "station.martinrue.com/",
                                "theunixzoo.co.uk/",
                                "redterminal.org/",
                                "astrobotany.mozz.us/app/pond",
                                "astrobotany.mozz.us/",
                                "station.martinrue.com/davep/notifications",
                                "station.martinrue.com/davep/followers",
                                "station.martinrue.com/davep/",
                                "geminiprotocol.net/",
                                "geminiprotocol.net/docs/",
                                "geminiprotocol.net/docs/gemtext-specification.gmi",
                            ]
                        )
                    ]
                )
            )
        )
    )


##############################################################################
# Create the Rogallo app with the specified command line arguments.
def make_app(
    viewing: str = "features", with_fake_history: bool = True, **config_overrides: Any
) -> Rogallo:
    save_naviagation_history(NavigationHistory([]))
    save_command_history(CommandLineHistory([]))
    if with_fake_history:
        fake_history()
    else:
        save_location_history(LocationHistory([]))
    with update_configuration() as config:
        # Spin up a default configuration.
        defaults = Configuration()
        for prop in fields(Configuration):
            setattr(config, prop.name, getattr(defaults, prop.name))
        # Override some details that are better for the docs.
        config.home_page = "gemini://localhost/"
        config.theme = "textual-mono"
        config.cache_ttl = 1
        # Then apply any overrides that were passed in.
        for prop, value in config_overrides.items():
            setattr(config, prop, value)
    if viewing and "." not in viewing:
        viewing = f"{viewing}.gmi"
    return Rogallo(
        Namespace(
            command="open",
            location=f"gemini://localhost/{viewing}",
            theme=None,
        )
        if viewing
        else Namespace(command="", theme=None)
    )


### maker.py ends here
