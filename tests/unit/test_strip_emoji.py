"""Unit tests for the content filter."""

##############################################################################
# Pytest imports.
from pytest import mark

##############################################################################
# Local imports.
from rogallo.strip_emoji import strip_emoji


##############################################################################
@mark.parametrize(
    "source, result",
    [
        # --- Basic & Spacing Cases ---
        ("", ""),
        (" ", " "),
        ("   ", "   "),
        ("No emoji here.", "No emoji here."),
        ("💩", ""),
        ("💩 ", ""),
        (" 💩", " "),
        ("💩💩💩💩💩", ""),
        ("💩 💩 💩 💩 💩 ", ""),
        ("😄 Hello", "Hello"),
        ("Hello, world! 🌍", "Hello, world! "),
        ("Hello 😄 world", "Hello world"),
        ("Multiple emojis 😄😎👍", "Multiple emojis "),
        ("Emoji with space 😄 ", "Emoji with space "),
        # --- Code Syntax & Math (Must Be Preserved) ---
        ("`code` and `variable`", "`code` and `variable`"),
        ("`foo` is a function", "`foo` is a function"),
        ("```python\nprint('hello')\n```", "```python\nprint('hello')\n```"),
        ("x ^ 2 and 2^3", "x ^ 2 and 2^3"),
        ("Item #1 and score: 100%", "Item #1 and score: 100%"),
        # --- Typography, Legal & Units (Must Be Preserved) ---
        ("Acme™ Corp", "Acme™ Corp"),
        ("Copyright © 2026, Rogallo®", "Copyright © 2026, Rogallo®"),
        ("Boiling point: 100 °C or 212 °F", "Boiling point: 100 °C or 212 °F"),
        ("Invoice № 12345", "Invoice № 12345"),
        ("Value ½ or ¼, Chapter Ⅳ", "Value ½ or ¼, Chapter Ⅳ"),
        # --- Keyboard Shortcuts & Terminal UI (Must Be Preserved) ---
        ("Press ⌘ + ⌥ + ⌫ or ⇧ + ⏎", "Press ⌘ + ⌥ + ⌫ or ⇧ + ⏎"),
        ("Directions: ← ↑ → ↓ ↔ ↕ ↗ ↘", "Directions: ← ↑ → ↓ ↔ ↕ ↗ ↘"),
        (
            "Items: ■ Square, ▲ Triangle, ● Circle, ◆ Diamond",
            "Items: ■ Square, ▲ Triangle, ● Circle, ◆ Diamond",
        ),
        ("┌───┬───┐\n│ A │ B │\n└───┴───┘", "┌───┬───┐\n│ A │ B │\n└───┴───┘"),
        ("Progress: [████░░░░]", "Progress: [████░░░░]"),
        ("Sparkline: ⠋ ⠙ ⠹ ⠸ ⠼ ⠴ ⠦ ⠧ ⠇ ⠏", "Sparkline: ⠋ ⠙ ⠹ ⠸ ⠼ ⠴ ⠦ ⠧ ⠇ ⠏"),
        ("漢字 (水 氵 ⺁ ⺂)", "漢字 (水 氵 ⺁ ⺂)"),
        # --- Clocks, Watches & Timers (Must Be Stripped) ---
        ("Time: ⌚ 12:00", "Time: 12:00"),
        ("Please wait ⌛...", "Please wait ..."),
        ("Wake up! ⏰", "Wake up! "),
        ("Lap time: ⏱ 00:42", "Lap time: 00:42"),
        ("Loading ⏳ now", "Loading now"),
        # --- Media Controls (Must Be Stripped) ---
        ("Controls: ⏩ ⏪ ⏸ ⏹ ⏺", "Controls: "),
        # --- Classic Symbols & Dingbats (Must Be Stripped) ---
        (
            "Coffee ☕ break on a ☀️ sunny day with ⚡ lightning",
            "Coffee break on a sunny day with lightning",
        ),
        (
            "Release ✨ features, mail ✉️, pencil ✏️, love ❤️",
            "Release features, mail , pencil , love ",
        ),
        ("Cut ✂️ here, fly ✈️ there", "Cut here, fly there"),
        # --- Complex & Modern Emoji Sequences (Must Be Stripped) ---
        ("Thumbs up 👍🏽 and waving 👋🏻", "Thumbs up and waving "),
        ("Coder 🧑‍💻, family 👨‍👩‍👧‍👦, pride 🏳️‍🌈", "Coder , family , pride "),
        ("Couple 🧑🏻‍🤝‍🧑🏿 walking", "Couple walking"),
        ("Scotland 🏴󠁧󠁢󠁳󠁣󠁴󠁿 flag", "Scotland flag"),
        ("Top 🔟 list", "Top list"),
    ],
)
def test_strip_emoji(source: str, result: str) -> None:
    """Test the strip_emoji utility function."""
    assert strip_emoji(source) == result


### test_strip_emoji.py ends here
