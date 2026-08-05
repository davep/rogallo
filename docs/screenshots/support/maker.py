"""Provides code for building a screenshot-ready Rogallo instance."""

import os
from argparse import Namespace
from dataclasses import fields
from datetime import datetime, timedelta
from json import dumps
from pathlib import Path
from random import randint
from typing import Any

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
# Work our the root of the documentation directory and the build directory.
docs_dir = Path(__file__).parent.parent.parent
docs_build_dir = docs_dir / "build"

##############################################################################
# Set the XDG_ to point at an isolated build environment for the
# screenshots. I don't want to mess with an actual installation of Rogallo.
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
(themes_dir() / "white.json").write_text(
    dumps(
        {
            "name": "terminal-white",
            "primary": "#E0E8F0",
            "secondary": "#A0ACB8",
            "accent": "#FFFFFF",
            "foreground": "#D0D8E0",
            "background": "#000000",
            "surface": "#0C0F12",
            "panel": "#161B20",
            "success": "#E0E8F0",
            "warning": "#F0F0D0",
            "error": "#5A3838",
            "dark": True,
            "luminosity_spread": 0.15,
            "text_alpha": 0.95,
            "variables": {
                "border": "#E0E8F0",
                "border-blurred": "#3A4450",
                "block-cursor-foreground": "#000000",
                "block-cursor-background": "#E0E8F0",
                "block-cursor-text-style": "none",
                "input-cursor-foreground": "#000000",
                "input-cursor-background": "#FFFFFF",
                "input-selection-background": "#A0ACB8 40%",
                "input-selection-foreground": "#000000",
                "screen-selection-background": "#A0ACB8 40%",
                "screen-selection-foreground": "#D0D8E0",
                "footer-background": "#0C0F12",
                "footer-key-foreground": "#E0E8F0",
                "footer-description-foreground": "#D0D8E0",
                "button-color-foreground": "#000000",
                "button-focus-text-style": "reverse",
                "foreground-muted": "#3A4450",
                "scrollbar": "#A0ACB8",
                "scrollbar-hover": "#E0E8F0",
                "scrollbar-active": "#FFFFFF",
                "scrollbar-background": "#000000",
                "scrollbar-background-hover": "#0C0F12",
                "scrollbar-background-active": "#161B20",
                "scrollbar-corner-color": "#000000",
            },
        },
        indent=4,
    )
)
(themes_dir() / "amber.json").write_text(
    dumps(
        {
            "name": "terminal-amber",
            "primary": "#FFB000",
            "secondary": "#C88200",
            "accent": "#FFC947",
            "foreground": "#FFC107",
            "background": "#000000",
            "surface": "#140E00",
            "panel": "#241800",
            "success": "#FFB000",
            "warning": "#FFDC00",
            "error": "#593800",
            "dark": True,
            "luminosity_spread": 0.15,
            "text_alpha": 0.95,
            "variables": {
                "block-cursor-background": "#FFB000",
                "block-cursor-foreground": "#000000",
                "block-cursor-text-style": "none",
                "border": "#FFB000",
                "border-blurred": "#4D3300",
                "button-color-foreground": "#000000",
                "button-focus-text-style": "reverse",
                "footer-background": "#140E00",
                "footer-description-foreground": "#FFC107",
                "footer-key-foreground": "#FFB000",
                "foreground": "#FFC107",
                "foreground-muted": "#4D3300",
                "input-cursor-background": "#FFC947",
                "input-cursor-foreground": "#000000",
                "input-selection-background": "#C88200 40%",
                "input-selection-foreground": "#000000",
                "screen-selection-background": "#C88200 40%",
                "screen-selection-foreground": "#FFC107",
                "scrollbar": "#C88200",
                "scrollbar-active": "#FFC947",
                "scrollbar-background": "#000000",
                "scrollbar-background-active": "#241800",
                "scrollbar-background-hover": "#140E00",
                "scrollbar-corner-color": "#000000",
                "scrollbar-hover": "#FFB000",
                "text": "#FFC107",
                "text-disabled": "#4D3300",
                "text-muted": "#4D3300",
            },
        },
        indent=4,
    )
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
    return Rogallo(
        Namespace(
            command="open",
            location=f"gemini://localhost/{viewing}.gmi",
            theme=None,
        )
        if viewing
        else Namespace(command="", theme=None)
    )


### maker.py ends here
