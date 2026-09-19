"""Screenshot to show the command line on top."""

from support.maker import Configuration, make_app

app = make_app(general=Configuration(command_line_on_top=True))

if __name__ == "__main__":
    app.run()

### command_line_top_screenshot.py ends here
