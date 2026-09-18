# Displayable content types

By default Rogallo only considers a narrow set of MIME types as displayable
in the application. In the event that you need to expand this list, you can
add a `displayable-content-types.yaml` file to the [configuration
directory](./index.md). This file should contain a list of MIME types you
want Rogallo to directly handle.

!!! note

    There is a hard-coded set of types that will always be handled;
    creating and populating this file *adds* to that list.

An example file, that adds more MIME types, might look like this:

```yaml
- "application/octet-stream"
- "message/rfc822"
- "application/javascript"
- "application/ecmascript"
- "application/x-ecmascript"
- "application/x-javascript"
```

!!! important

    Rogallo is currently only capable of displaying text-based content,
    showing either rendered Gemtext or plain text. Adding other MIME types
    might cause unwanted or unpredictable results.

[//]: # (content_types.md ends here)
