# The viewer

## Introduction

The viewer is the main widget in Rogallo's display. If you are viewing a
[Gemini page](./gemini.md), a [Gopher server](./gopher.md) or the response
from a [Finger server](./finger.md), this is where the result will be
displayed.

When it has focus, the viewer has a number of keys that let you navigate the
content. Where possible, many of the navigation keys that you might have
muscle-memory for are available. You can always check what keys are
available by calling on the `Help` command (bound to <kbd>F1</kbd> by
default).

```{.textual path="docs/screenshots/main_screenshot.py" title="Viewer help" lines=55 columns=100 press="f1"}
```

## Link navigation

When viewing a Gemini page or a Gopher menu, often there will be links
embedded in the page. There are a number of ways that these can be
navigated.

### Next/previous navigation

Links within the viewer are navigable widgets, just like other elements in
[Rogallo's user interface](./ui.md). As such you can move between them with
<kbd>Tab</kbd> and <kbd>Shift</kbd>+<kbd>Tab</kbd>. Because these keys will
eventually navigate you out of the viewer and on to other widgets in the
user interface, there are some other keys that let you move between links
and stay within the viewer:

- <kbd>←</kbd>, <kbd>Shift</kbd>+<kbd>↑</kbd>, <kbd>L</kbd> - All navigate
  to the previous link.
- <kbd>→</kbd>, <kbd>Shift</kbd>+<kbd>↓</kbd>, <kbd>l</kbd> - All navigate
  to the next link.

### Jump to link

To speed up navigating to a specific link, Rogallo also provides a method of
jumping to a specific link. By default each link in a document will have a
numbered label shown to the right of the viewer (the position [is
configurable](./configuration.md#link-jumps)).

```{.textual path="docs/screenshots/stripes_screenshot.py" title="Links with labels" lines=30 columns=70}
```

To jump to that link, simply type its number.

```{.textual path="docs/screenshots/stripes_screenshot.py" title="A highlighted link after typing its number" lines=30 columns=70 press="5"}
```

## Configuration

### Filtering out pre-formatted text

Because pre-formatted text can be used to generate site logos and similar,
this can sometimes mean that you're faced with viewing the same ASCII art
over and over again, that uses up vertical space, and means it takes longer
to get to the content of a site. With this in mind Rogallo has a facility
for hiding specific pre-formatted text. It is based on the idea that such
pre-formatted blocks will have alt-text, and that we will normally only want
to do it for a specific URI. As an example: suppose I wanted to hide *my*
avatar image on [Station](gemini://station.martinrue.com/), and also the
site logo to save some space, I can set the following in the configuration
file:

```json
"hide_preformatted": [
    [
        "gemini://station.martinrue.com/",
        "Station logo"
    ],
    [
        "gemini://station.martinrue.com/davep",
        "User image"
    ]
]
```

As you can see, the filters are defined as a list of lists. The first value
in each is the URI to match. This will match *that location and all below
it*. So in the above `gemini://station.martinrue.com/` would match that
location, and also `gemini://station.martinrue.com/davep` and
`gemini://station.martinrue.com/example-user` and so on. The second value is
the alt-text for the pre-formatted text.

[//]: # (viewer.md ends here)
