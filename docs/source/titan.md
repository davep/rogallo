# Titan

## Introduction

Closely related to the [Gemini Protocol](./gemini.md), Rogallo also has
support for the [Titan Protocol](https://communitywiki.org/wiki/Titan). When
presented with a `titan://` URI Rogallo will allow you to enter and submit
text, or select and upload a file.

## Text entry and submission

The Titan-related dialog has a tabbed view. If the first tab is selected the
intention is that you enter your text and submit it.

```{.textual path="docs/screenshots/titan_screenshot.py" title="Titan text entry" lines=50 columns=100 press="right,enter,tab"}
```

## File upload submission

If you select the `File` tab you have the ability to select a file from the
filesystem and specify its mime type (this will be set for you when you
select a file).

```{.textual path="docs/screenshots/titan_screenshot.py" title="Titan file uploading" lines=50 columns=100 press="right,enter,ctrl+f,tab,tab"}
```

[//]: # (titan.md ends here)
