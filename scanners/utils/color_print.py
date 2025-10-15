class Colors:
    """ANSI color codes for terminal output."""

    RESET = "\033[0m"

    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

    BACKGROUND_BLACK = "\033[40m"
    BACKGROUND_RED = "\033[41m"
    BACKGROUND_GREEN = "\033[42m"
    BACKGROUND_YELLOW = "\033[43m"
    BACKGROUND_BLUE = "\033[44m"
    BACKGROUND_MAGENTA = "\033[45m"
    BACKGROUND_CYAN = "\033[46m"
    BACKGROUND_WHITE = "\033[47m"

    BRIGHT_BACKGROUND_BLACK = "\033[100m"
    BRIGHT_BACKGROUND_RED = "\033[101m"
    BRIGHT_BACKGROUND_GREEN = "\033[102m"
    BRIGHT_BACKGROUND_YELLOW = "\033[103m"
    BRIGHT_BACKGROUND_BLUE = "\033[104m"
    BRIGHT_BACKGROUND_MAGENTA = "\033[105m"
    BRIGHT_BACKGROUND_CYAN = "\033[106m"
    BRIGHT_BACKGROUND_WHITE = "\033[107m"


def print_colored(text: str, color_code: str) -> None:
    """Print text in specified color.

    Args:
        text: The text to print.
        color_code: ANSI color code to apply.
    """
    print(f"{color_code}{text}{Colors.RESET}")


def print_red(text: str) -> None:
    """Print text in red color.

    Args:
        text: The text to print.
    """
    print_colored(text, Colors.RED)


def print_green(text: str) -> None:
    """Print text in green color.

    Args:
        text: The text to print.
    """
    print_colored(text, Colors.GREEN)


def print_yellow(text: str) -> None:
    """Print text in yellow color.

    Args:
        text: The text to print.
    """
    print_colored(text, Colors.YELLOW)


def print_blue(text: str) -> None:
    """Print text in blue color.

    Args:
        text: The text to print.
    """
    print_colored(text, Colors.BLUE)


def print_magenta(text: str) -> None:
    """Print text in magenta color.

    Args:
        text: The text to print.
    """
    print_colored(text, Colors.MAGENTA)


def print_cyan(text: str) -> None:
    """Print text in cyan color.

    Args:
        text: The text to print.
    """
    print_colored(text, Colors.CYAN)


def print_white(text: str) -> None:
    """Print text in white color.

    Args:
        text: The text to print.
    """
    print_colored(text, Colors.WHITE)


def print_black(text: str) -> None:
    """Print text in black color.

    Args:
        text: The text to print.
    """
    print_colored(text, Colors.BLACK)


def print_bright_red(text: str) -> None:
    """Print text in bright red color.

    Args:
        text: The text to print.
    """
    print_colored(text, Colors.BRIGHT_RED)


def print_bright_green(text: str) -> None:
    """Print text in bright green color.

    Args:
        text: The text to print.
    """
    print_colored(text, Colors.BRIGHT_GREEN)


def print_bright_yellow(text: str) -> None:
    """Print text in bright yellow color.

    Args:
        text: The text to print.
    """
    print_colored(text, Colors.BRIGHT_YELLOW)


def print_bright_blue(text: str) -> None:
    """Print text in bright blue color.

    Args:
        text: The text to print.
    """
    print_colored(text, Colors.BRIGHT_BLUE)


def print_bright_magenta(text: str) -> None:
    """Print text in bright magenta color.

    Args:
        text: The text to print.
    """
    print_colored(text, Colors.BRIGHT_MAGENTA)


def print_bright_cyan(text: str) -> None:
    """Print text in bright cyan color.

    Args:
        text: The text to print.
    """
    print_colored(text, Colors.BRIGHT_CYAN)


def print_bright_white(text: str) -> None:
    """Print text in bright white color.

    Args:
        text: The text to print.
    """
    print_colored(text, Colors.BRIGHT_WHITE)
