# Custom themes

## Introduction

Rogallo is built using the [Textual
framework](https://textual.textualize.io), and Textual has some degree of
support for [themes](https://textual.textualize.io/guide/design/). Rogallo
makes use of this, and the ability to [register
themes](https://textual.textualize.io/guide/design/#registering-a-theme), to
provide a way to add your own themes to the application.

## Themes location

To add your own themes you create `json` files in a `themes` directory below
where the [configuration file lives](./configuration.md). For example:

```sh
~/.config/rogallo/themes$ ls -1
amber.json
cbm64.json
cyan.json
green.json
speccy.json
teletext.json
turbo.json
white-inverted.json
white.json
```

## Theme file content

A theme file should be a JSON document that contains the key/value pairs
needed to [provide the required variables for a Textual
theme](https://textual.textualize.io/guide/design/#theme-variables). An
example could be this:

```json
--8<-- "docs/build/config/rogallo/themes/white.json"
```

!!! tip "Getting help with making a theme"

    If you are trying to create a theme and are struggling with some aspect of it,
    please don't hesitate to [drop into the Q&A section of discussions and
    ask for help](https://github.com/davep/rogallo/discussions/categories/q-a). If I
    can figure out how to do it, I'll let you know (and likely improve the
    documentation).

## Using a theme

Once you've created one or more theme files in the theme directory, just use
the `ChangeTheme` command (bound to <kbd>F9</kbd> by default) and pick the
theme.

!!! danger "If you made a theme but it's missing"

    If you've created a theme and it doesn't show in the list of available
    themes, this means you've made a mistake, perhaps resulting in invalid
    JSON. Review your file, fix any problems, and try again.

As an example, if we load up Rogallo and select the theme example given
above, we should see:

=== "Using a white-on-black theme"

    ```{.textual path="docs/screenshots/main_screenshot.py" title="Rogallo in white" lines=35 columns=90 press="f9,t,e,r,m,i,n,a,l,-,w,h,i,t,e,enter"}
    ```

=== "white.json"

    ```json
    --8<-- "docs/build/config/rogallo/themes/white.json"
    ```

Or, if you selected a similar theme, made to make Rogallo look like it was
running on an amber terminal:

=== "Using an amber screen theme"

    ```{.textual path="docs/screenshots/main_screenshot.py" title="Rogallo in amber" lines=35 columns=90 press="f9,t,e,r,m,i,n,a,l,-,a,m,b,e,r,enter"}
    ```

=== "amber.json"

    ```json
    --8<-- "docs/build/config/rogallo/themes/amber.json"
    ```

Another option might be a classic green screen:

=== "Using a green screen theme"

    ```{.textual path="docs/screenshots/main_screenshot.py" title="Rogallo in green" lines=35 columns=90 press="f9,t,e,r,m,i,n,a,l,-,g,r,e,e,n,enter"}
    ```

=== "green.json"

    ```json
    --8<-- "docs/build/config/rogallo/themes/green.json"
    ```

Or how about something that invokes the age of microcomputers?

=== "Using a theme inspired by the CBM64"

    ```{.textual path="docs/screenshots/main_screenshot.py" title="Micro colourful" lines=35 columns=90 press="f9,m,i,c,r,o,-,c,b,m,6,4,enter"}
    ```

=== "cbm64.json"

    ```json
    --8<-- "docs/build/config/rogallo/themes/cbm64.json"
    ```

## Sharing themes

If you'd like to share a theme you've made, please feel free to post a
screenshot, the JSON, and any other details, [in the themes discussion
group](https://github.com/davep/rogallo/discussions/categories/custom-themes).

[//]: # (custom-themes.md ends here)
