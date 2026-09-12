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

## Toolbar configuration

The toolbar is configured in a file called `toolbar.yaml`, which can be
found in the [configuration directory](../configuration/directory.md).

!!! note

    The default `toolbar.yaml` file will be created for you the first time
    you run Rogallo.

## Toolbar content

The buttons that make up the content of the toolbar are configured with the
`buttons` value in the `toolbar.yaml` file. It is a list of `command` and
`label` properties, where `command` is one of the [bindable
commands](../configuration/bindings.md#bindable-commands) and `label` is the
label you want to appear in the button.

The settings for the default buttons look like this:

```yaml
buttons:
- command: GoHome
  label: "\u2302"
- command: Reload
  label: "\u21BB"
- command: Backward
  label: "\u25C0\u25C0"
- command: Forward
  label: "\u25B6\u25B6"
- command: GoToParent
  label: "\u2191"
- command: GoToRoot
  label: "\u21C8"
- command: SearchHistory
  label: "\u25F7"
- command: SearchBookmarks
  label: "\u2605"
- command: ToggleView
  label: "\u21CB"
```

To configure the content of the toolbar, edit this list to add or remove
buttons.

## Hiding the toolbar

If you are someone who is keyboard-only and has no use for the toolbar, you
can turn it off with the `visible` setting:

```yaml
visible: true
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

```yaml
show_tooltips: true
```

Set it to `false` to remove the tooltips.

## Using the toolbar with the keyboard

By default the toolbar can't be used via the keyboard; it is intended to be
a mouse-oriented feature. All of the commands that you could add to the
toolbar will already have keyboard bindings so the intention is that you
learn and use them (or run the commands via the command palette).

However, if you would prefer to be able to use the keyboard to navigate into
the toolbar, this can be turned on by changing this configuration setting:

```yaml
can_get_focus: false
```

Setting this to `true` means that all of the toolbar buttons will be capable
of receiving focus and being navigable like all other UI elements that are
capable of receiving focus.

[//]: # (toolbar.md ends here)
