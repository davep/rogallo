"""Screenshot to show the toolbar removed."""

from support.maker import ToolbarConfiguration, make_app

app = make_app(toolbar=ToolbarConfiguration(visible=False))

if __name__ == "__main__":
    app.run()

### no_toolbar_screenshot.py ends here
