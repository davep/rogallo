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
cga.json
cobalt.json
green.json
inverted-white.json
olive.json
organge.json
plasma.json
rainbow.json
speccy.json
turbo.json
vic20.json
white.json
```

## Theme file content

A theme file should be a JSON document that contains the key/value pairs
needed to [provide the required variables for a Textual
theme](https://textual.textualize.io/guide/design/#theme-variables). An
example could be this:

```json
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
  "dark": true,
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
    "scrollbar-corner-color": "#000000"
  }
}
```

!!! note

    As of the time of writing, some of the theming support in Textual
    remains sparsely documented. As such it's part guesswork, part
    code-reading, that is needed to create a workable theme. If you are
    trying to create a theme and are struggling with some aspect of it,
    please don't hesitate to [drop into the Q&A section of discussions and
    ask for
    help](https://github.com/davep/rogallo/discussions/categories/q-a). If I
    can figure out how to do it, I'll let you know (and likely improve the
    documentation).

## Using a theme

Once you've created one or more theme files in the theme directory, just use
the `ChangeTheme` command (bound to <kbd>F9</kbd> by default) and pick the
theme.

!!! danger "Missing theme"

    If you've created a theme and it doesn't show in the list of available
    themes, this means you've made a mistake, perhaps resulting in invalid
    JSON. Review your file, fix any problems, and try again.

As an example, if we load up Rogallo and select the theme example given
above, we should see:

```{.textual path="docs/screenshots/main_screenshot.py" title="Rogallo in white" lines=35 columns=90 press="f9,t,e,r,m,i,n,a,l,-,w,h,i,t,e,enter"}
```

Or if you selected a similar theme, made to make Rogallo look like it was
running on an amber terminal:

```{.textual path="docs/screenshots/main_screenshot.py" title="Rogallo in amber" lines=35 columns=90 press="f9,t,e,r,m,i,n,a,l,-,a,m,b,e,r,enter"}
```

## Sharing themes

If you'd like to share a theme you've made, please feel free to post a
screenshot, the JSON, and any other details, [in the themes discussion
group](https://github.com/davep/rogallo/discussions/categories/custom-themes).

[//]: # (custom-themes.md ends here)
