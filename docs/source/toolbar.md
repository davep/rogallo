# The toolbar

## Introduction

While Rogallo is designed to be keyboard-friendly and, where possible,
keyboard-first, it also has mouse support. If you are someone who tends to
use the mouse more than the keyboard, you'll probably find yourself wanting
quick and easy access to common commands, in a way that you can simply click
on them.

With this in mind, Rogallo has an optional mouse-oriented toolbar. This can
be seen at the top of the screen.

```{.textual path="docs/screenshots/main_screenshot.py" title="The toolbar" lines=40 columns=85}
```

## Toolbar content

The content of the toolbar can be configured in the configuration file,
using the `toolbar_contents` setting. The value is a list of [bindable
commands](./configuration.md#bindable-commands), along with an optional text
to show in the toolbar. By default the value is set to this:

```json
"toolbar_contents": [
    [
        "GoHome",
        "\u2302"
    ],
    [
        "Reload",
        "\u21bb"
    ],
    [
        "Backward",
        "\u25c0\u25c0"
    ],
    [
        "Forward",
        "\u25b6\u25b6"
    ],
    [
        "GoToParent",
        "\u2191"
    ],
    [
        "GoToRoot",
        "\u21c8"
    ],
    [
        "SearchHistory",
        "\u25f7"
    ],
    [
        "SearchBookmarks",
        "\u2605"
    ],
    [
        "ToggleView",
        "\u21cb"
    ]
]
```

In each case it's a command name, along with the text to show in the toolbar
(in these cases, icon-type values to help save space). To configure the
content of the toolbar, edit the configuration file to add or remove
commands.

## Hiding the toolbar

If you are someone who is keyboard-only and has no use for the toolbar, you
can turn it off with this configuration file value:

```json
"toolbar_visible": true,
```

Set it to `false` to hide the toolbar.

```{.textual path="docs/screenshots/no_toolbar_screenshot.py" title="Hidden toolbar" lines=40 columns=85}
```

## Turning off tooltips

By default, the toolbar will show tooltips when you hover the mouse cursor
over a button.

```{.textual path="docs/screenshots/main_screenshot.py" title="Mouse hovering over the last toolbar button" lines=35 columns=90 hover="CommandButton:last-of-type"}
```

If you would prefer that these tooltips don't show, change this
configuration file setting:

```json
"toolbar_tooltips": true
```

## Using the toolbar with the keyboard

By default the toolbar can't be used via the keyboard; it is intended to be
a mouse-oriented feature. All of the commands that you could add to the
toolbar will already have keyboard bindings so the intention is that you
learn and use them (or run the commands via the command palette).

However, if you would prefer to be able to use the keyboard to navigate into
the toolbar, this can be turned on by changing this configuration setting:

```json
"toolbar_can_get_focus": false,
```

Setting this to `true` means that all of the toolbar buttons will be capable
of receiving focus and being navigable like all other UI elements that are
capable of receiving focus.

[//]: # (toolbar.md ends here)
