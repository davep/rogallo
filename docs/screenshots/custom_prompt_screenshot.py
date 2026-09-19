"""Screenshot showing a custom prompt."""

from support.maker import GeneralConfiguration, make_app

app = make_app(general=GeneralConfiguration(command_line_prompt="\U0001f680"))

if __name__ == "__main__":
    app.run()

### custom_prompt_screenshot.py ends here
