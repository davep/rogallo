# Rogallo Markdown example

## A paragraph

This is a paragraph.
This is some more of that paragraph.
Here's the final sentence in that paragraph.

## Links

Links [are handled just fine too](gemini://tilde.team/~davep).
As well as done [as markup](https://blog.davep.org/), they can also appear inline: gopher://tilde.team/1/~davep/
-- while that Gopher link there isn't markup, it is detected and linked.

## Tables

| Protocol | Documentation                      |
|----------|------------------------------------|
| Gemini   | https://rogallo.davep.dev/gemini/  |
| Gopher   | https://rogallo.davep.dev/gopher/  |
| Finger   | https://rogallo.davep.dev/finger/  |
| Spartan  | https://rogallo.davep.dev/spartan/ |
| Nex      | https://rogallo.davep.dev/nex/     |

## Blockquotes

To quote myself:

> Rogallo supports blockquotes in Markdown.

There, I said it.

## Preformatted text

```python
def calculate_collatz_sequence(starting_number: int) -> list[int]:
    if starting_number < 1:
        raise ValueError("Starting number must be a positive integer.")

    sequence = [starting_number]
    current_number = starting_number

    while current_number != 1:
        if current_number % 2 == 0:
            current_number = current_number // 2
        else:
            current_number = 3 * current_number + 1
        sequence.append(current_number)

    return sequence
```

