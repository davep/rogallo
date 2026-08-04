# Gopher

## Introduction

Rogallo has support for visiting Gopher servers. Much like when [visiting a
Gemini server](./gemini.md), you can type in the URI of the location you
wish to visit. Gopher URIs begin with `gopher://`.

```{.textual path="docs/screenshots/empty_screenshot.py" title="Entering a Gopher URI" lines=30 columns=90 press="g,o,p,h,e,r,:,/,/,l,o,c,a,l,h,o,s,t"}
```

```{.textual path="docs/screenshots/empty_screenshot.py" title="After pressing Enter" lines=30 columns=90 press="g,o,p,h,e,r,:,/,/,l,o,c,a,l,h,o,s,t,:,7,0,7,0,enter"}
```

!!! note

    There is a small cheat in the above example. You'll notice the `7070` in
    the URI in the second screenshot. This is simply down to that being the
    port of the server used to generate this documentation. Under normal
    circumstances you would not need to enter the port (which is `70` by
    default, for Gopher).

## Supported item types

Rogallo has direct support for a number of Gopher item types. These types
will be handled by or rendered in Rogallo itself. Any other type will be
turned into the most appropriate URI and passed to the operating system to
be handled by other tools.

### `0` - Text

If an item is declared to be text, Rogallo will assume that it is safe to be
treated as a `text/plain` type and, when selected, it will be shown in the
viewer.

```{.textual path="docs/screenshots/empty_screenshot.py" title="Viewing a text file" lines=30 columns=90 press="g,o,p,h,e,r,:,/,/,l,o,c,a,l,h,o,s,t,:,7,0,7,0,/,0,/,a,b,o,u,t,.,t,x,t,enter"}
```

### `1` - Menu (directory)

If an item is declared to be a menu, Rogallo will follow the URI.

```{.textual path="docs/screenshots/empty_screenshot.py" title="Viewing another menu" lines=30 columns=90 press="g,o,p,h,e,r,:,/,/,l,o,c,a,l,h,o,s,t,:,7,0,7,0,/,1,/,d,o,c,s,enter"}
```

### `7` - Search

If an item is declared to be a search, when selected, Rogallo will prompt
you for the query before following the link.

```{.textual path="docs/screenshots/empty_screenshot.py" title="Entering a search query" lines=30 columns=90 press="g,o,p,h,e,r,:,/,/,l,o,c,a,l,h,o,s,t,:,7,0,7,0,/,enter,4,enter"}
```

### `h` - HTML

If an item is declared as being HTML, and the selector starts with `URL:`,
what follows the `URL:` will be turned into a URI that can be followed.

[//]: # (gopher.md ends here)
