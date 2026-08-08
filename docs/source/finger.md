# Finger

## Introduction

Rogallo has support for displaying information returned from a Finger
server.

## `finger://` URIs

Rogallo will handle any valid `finger://` URI, either as a link to be
followed from content returned by a [Gemini](./gemini.md),
[Spartan](./spartan.md) or [Gopher](./gopher.md) server, or as entered in
the [command line](./command-line.md).

```{.textual path="docs/screenshots/empty_screenshot.py" title="Entering a Finger URI" lines=30 columns=90 press="f,i,n,g,e,r,:,/,/,l,o,c,a,l,h,o,s,t,/,d,a,v,e,p"}
```

```{.textual path="docs/screenshots/empty_screenshot.py" title="After pressing Enter" lines=30 columns=90 press="f,i,n,g,e,r,:,/,/,l,o,c,a,l,h,o,s,t,:,7,9,7,9,/,d,a,v,e,p,enter"}
```

## Finger command

There is also support for a `!finger` command in the [command
line](./command-line.md). The parameter it takes is the more traditional
`user@host` format.

```{.textual path="docs/screenshots/empty_screenshot.py" title="Using the finger command" lines=30 columns=90 press="!,f,i,n,g,e,r, ,d,a,v,e,p,@,l,o,c,a,l,h,o,s,t"}
```

Note that this *expects* that the finger server is listening on port 79.

[//]: # (finger.md ends here)
