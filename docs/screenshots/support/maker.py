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
            "primary": "#D8D8D8",
            "secondary": "#9E9E9E",
            "accent": "#C4C4C4",
            "foreground": "#B8B8B8",
            "background": "#000000",
            "surface": "#121212",
            "panel": "#1E1E1E",
            "success": "#D8D8D8",
            "warning": "#C4C4C4",
            "error": "#4A4A4A",
            "dark": True,
            "luminosity_spread": 0.15,
            "text_alpha": 0.95,
            "variables": {
                "block-cursor-background": "#D8D8D8",
                "block-cursor-foreground": "#000000",
                "block-cursor-text-style": "none",
                "border": "#D8D8D8",
                "border-blurred": "#404040",
                "button-color-foreground": "#000000",
                "button-focus-text-style": "reverse",
                "footer-background": "#121212",
                "footer-description-foreground": "#B8B8B8",
                "footer-key-foreground": "#D8D8D8",
                "foreground": "#B8B8B8",
                "foreground-muted": "#404040",
                "input-cursor-background": "#C4C4C4",
                "input-cursor-foreground": "#000000",
                "input-selection-background": "#9E9E9E 40%",
                "input-selection-foreground": "#000000",
                "screen-selection-background": "#9E9E9E 40%",
                "screen-selection-foreground": "#B8B8B8",
                "scrollbar": "#9E9E9E",
                "scrollbar-active": "#C4C4C4",
                "scrollbar-background": "#000000",
                "scrollbar-background-active": "#1E1E1E",
                "scrollbar-background-hover": "#121212",
                "scrollbar-corner-color": "#000000",
                "scrollbar-hover": "#D8D8D8",
                "text": "#B8B8B8",
                "text-disabled": "#404040",
                "text-muted": "#404040",
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
(themes_dir() / "green.json").write_text(
    dumps(
        {
            "name": "terminal-green",
            "primary": "#33FF33",
            "secondary": "#00AA44",
            "accent": "#66FF66",
            "foreground": "#33FF33",
            "background": "#000000",
            "surface": "#001A08",
            "panel": "#003311",
            "success": "#33FF33",
            "warning": "#CCFF33",
            "error": "#004D1A",
            "dark": True,
            "luminosity_spread": 0.15,
            "text_alpha": 0.95,
            "variables": {
                "block-cursor-background": "#33FF33",
                "block-cursor-foreground": "#000000",
                "block-cursor-text-style": "none",
                "border": "#33FF33",
                "border-blurred": "#004D1A",
                "button-color-foreground": "#000000",
                "button-focus-text-style": "reverse",
                "footer-background": "#001A08",
                "footer-description-foreground": "#33FF33",
                "footer-key-foreground": "#33FF33",
                "foreground": "#33FF33",
                "foreground-muted": "#004D1A",
                "input-cursor-background": "#66FF66",
                "input-cursor-foreground": "#000000",
                "input-selection-background": "#00AA44 40%",
                "input-selection-foreground": "#000000",
                "screen-selection-background": "#00AA44 40%",
                "screen-selection-foreground": "#33FF33",
                "scrollbar": "#00AA44",
                "scrollbar-active": "#66FF66",
                "scrollbar-background": "#000000",
                "scrollbar-background-active": "#003311",
                "scrollbar-background-hover": "#001A08",
                "scrollbar-corner-color": "#000000",
                "scrollbar-hover": "#33FF33",
                "text": "#33FF33",
                "text-disabled": "#004D1A",
                "text-muted": "#004D1A",
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
