# The viewer

## Introduction

The viewer is the main widget in Rogallo's display. If you are viewing a
[Gemini page](../protocols/gemini.md), a [Gopher server](../protocols/gopher.md) or the response
from a [Finger server](../protocols/finger.md), this is where the result will be
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
[Rogallo's user interface](./index.md). As such you can move between them with
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
configurable](#cosy-link-jumps)).

```{.textual path="docs/screenshots/stripes_screenshot.py" title="Links with labels" lines=30 columns=70}
```

To jump to that link, simply type its number.

```{.textual path="docs/screenshots/stripes_screenshot.py" title="A highlighted link after typing its number" lines=30 columns=70 press="5"}
```

Linking jumping and the numbers that let you jump are toggled with the
<kbd>J</kbd> (that's <kbd>Shift</kbd>+<kbd>J</kbd>) key.

### Link stripes

Placing the jump number labels to the right helps keep a readable flow of
text, but can possibly make it trickier to know which label matches which
link.

```{.textual path="docs/screenshots/stripes_screenshot.py" title="Links and labels with no stripes" lines=30 columns=70}
```

To help with this you can turn on "link stripes", which alternates the
background colour of links to help make them stand out and connect with
their labels. Press <kbd>s</kbd> to toggle the stripes.

```{.textual path="docs/screenshots/stripes_screenshot.py" title="Links with stripes" lines=30 columns=70 press="s"}
```

### Cosy link jumps

By default the numeric labels for the jumps are positioned to the right of
the display. This is done to keep a readable flow of text. While [link
stripes](#link-stripes) are provided to make it easier to know which label
goes with which link, some people might prefer the labels to really cosy up
with the links. The position can be toggled with
<kbd>Ctrl</kbd>+<kbd>j</kbd>.

```{.textual path="docs/screenshots/stripes_screenshot.py" title="Cosy link number labels" lines=30 columns=70 press="super+f8"}
```

## Emoji removal

Some people find the use of emoji in Gemtext off-putting. With this in mind,
when the viewer has focus, you can press <kbd>Ctrl</kbd>+<kbd>e</kbd> to
toggle them off and on.

So, if presented with this:

```{.textual path="docs/screenshots/emoji_screenshot.py" title="Lots of emoji" lines=30 columns=80}
```

and you press <kbd>Ctrl</kbd>+<kbd>e</kbd>, you get this:

```{.textual path="docs/screenshots/emoji_screenshot.py" title="Cleaned of emoji" lines=30 columns=80 press="ctrl+e"}
```

## ANSI escape sequence support

Rogallo supports ANSI escape sequences in the content of pages. This means
that sites can do all sorts of wonderfully colourful things:

```{.textual path="docs/screenshots/ansi_screenshot.py" title="Some fun with ANSI" lines=43 columns=80}
```

If you would prefer that ANSI escape sequences *aren't* processed, and
instead are stripped from the content, you can press <kbd>a</kbd> to toggle
support off or back on.

```{.textual path="docs/screenshots/ansi_screenshot.py" title="Turning off ANSI" lines=43 columns=80 press="a"}
```

Admittedly, in this case the stripped version isn't anywhere near as
interesting, but in most cases you'll get the content you were seeing, just
without colour.

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
site logo to save some space, I can set the following in `preformatted.yaml`
in the [configuration directory](../configuration/directory.md):

```yaml
hide:
- uri_prefix: "gemini://station.martinrue.com/"
  alt_text: "Station logo"
- uri_prefix: "gemini://station.martinrue.com/davep"
  alt_text: "User image"
```

As you can see, the filters are defined as a list of objects. The
`uri_prefix` property in each is the URI to match. This will match *that
location and all below it*. So in the above
`gemini://station.martinrue.com/` would match that location, and also
`gemini://station.martinrue.com/davep` and
`gemini://station.martinrue.com/example-user` and so on. The `alt_text`
property is the alt-text for the pre-formatted text.

### Blending pre-formatted text background

By default, for any pre-formatted text *with* alt-text, Rogallo will use a
background colour that is distinct from the background colour of the viewer.
On the other hand, by default, pre-formatted text without alt-text will use
the viewer's background. If you wish to change this, you can configure it
via `preformatted.yaml` in the [configuration
directory](../configuration/directory.md), using the `blend` setting. It
takes a list of alt-text values, and will blend any listed. By default it is
set to:

```yaml
blend_with_background:
- ''
```

If, for example, you wanted to blend `Station logo` and `User image` too:

```yaml
blend_with_background:
- ''
- 'Station logo'
- 'User image'
```

### Pre-formatted text tooltips

By default, when using a mouse, Rogallo will show any alt-text associated
with some pre-formatted text when you hover the mouse cursor over the block
of text.

```{.textual path="docs/screenshots/preformat_screenshot.py" title="Rogallo showing a pre-format tooltip" lines=35 columns=90 hover="GemtextPreformatted:last-of-type"}
```

If this feels too cluttered it can be turned off with the `tooltips` setting
in the `preformatted.yaml` file in the [configuration
directory](../configuration/directory.md). Valid values are `true` and
`false`, with `true` (show the tooltips) being the default.

```yaml
tooltips: true
```

### Markdown rendering

If Rogallo is served a Markdown file, it will convert it into Gemtext and
render it. This makes it easier to navigate links, etc.

```{.textual path="docs/screenshots/markdown_gemtext_screenshot.py" title="Viewing Markdown as Gemtext" lines=50 columns=90}
```

If you would prefer that Rogallo renders the text using its builtin Markdown
widget, you can set `convert_markdown_to_gemtext` in `general.yaml` (found
in the [configuration directory](../configuration/directory.md)) to `false`:

```yaml
convert_markdown_to_gemtext: false
```

The result of viewing Markdown will be more like this:

```{.textual path="docs/screenshots/markdown_widget_screenshot.py" title="Viewing Markdown" lines=50 columns=90}
```

While the result is more in keeping with the document being Markdown, it
will be trickier to navigate if you don't have a mouse (the issue being that
[Textual's Markdown widget](https://textual.textualize.io/widgets/markdown/)
is keyboard-hostile when it comes to navigation of links).

## Available bindings

The following actions can [have their bindings overridden](../configuration/bindings.md):

- `viewer.cancel_search` - Cancel the current search in the document
- `viewer.next_link` - Move forward through each of the links
- `viewer.previous_link` - Move backwards through each of the links
- `viewer.search_next` - Look for the next search hit in the document
- `viewer.start_search` - Start a search for text in the document
- `viewer.toggle_ansi` - Toggle whether ANSI escape sequences are handled in text content
- `viewer.toggle_cosy_link_numbers` - Toggle whether the numeric labels are displayed on the left or right of the link
- `viewer.toggle_emoji` - Toggle whether emoji are stripped from text content
- `viewer.toggle_link_numbers` - Toggle whether links are given numeric labels for jumping to them
- `viewer.toggle_stripe_links` - Toggle whether links are given alternating backgrounds

[//]: # (viewer.md ends here)
