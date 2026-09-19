"""Screenshot to show the command line on top."""

from support.maker import GeneralConfiguration, make_app

app = make_app(general=GeneralConfiguration(command_line_on_top=True))

if __name__ == "__main__":
    app.run()

### command_line_top_screenshot.py ends here
