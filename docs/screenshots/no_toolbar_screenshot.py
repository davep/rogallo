"""Screenshot to show the toolbar removed."""

from support.maker import make_app

app = make_app(toolbar_visible=False)

if __name__ == "__main__":
    app.run()

### no_toolbar_screenshot.py ends here
