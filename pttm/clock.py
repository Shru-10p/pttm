# Big blocky font digits for the clock
DIGITS = {
    '0': ["███", "█ █", "█ █", "█ █", "███"],
    '1': [" █ ", "██ ", " █ ", " █ ", "███"],
    '2': ["███", "  █", "███", "█  ", "███"],
    '3': ["███", "  █", "███", "  █", "███"],
    '4': ["█ █", "█ █", "███", "  █", "  █"],
    '5': ["███", "█  ", "███", "  █", "███"],
    '6': ["███", "█  ", "███", "█ █", "███"],
    '7': ["███", "  █", "  █", "  █", "  █"],
    '8': ["███", "█ █", "███", "█ █", "███"],
    '9': ["███", "█ █", "███", "  █", "███"],
    ':': ["   ", " █ ", "   ", " █ ", "   "],
    ' ': ["   ", "   ", "   ", "   ", "   "]
}

def make_clock_ascii(seconds: int) -> str:
    mins = seconds // 60
    secs = seconds % 60
    time_str = f"{mins:02d}:{secs:02d}"

    lines = ["", "", "", "", ""]
    for char in time_str:
        char_lines = DIGITS.get(char, DIGITS[' '])
        for idx in range(5):
            lines[idx] += char_lines[idx] + "  "

    return "\n".join(lines)
